from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, SymptomCheck, EyeDetection
from .prediction import detect_symptoms_in_text, predict_from_symptoms
from .serializers import LoginSerializer, RegisterSerializer, SymptomCheckSerializer
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
import base64
import os
from PIL import Image
import io
import requests

# Import YOLO
try:
    from ultralytics import YOLO
    import cv2
    import numpy as np
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

# Path to YOLO model
MODEL_PATH = os.environ.get(
    'EYE_MODEL_PATH',
    str(settings.BASE_DIR / 'models' / 'eye' / 'best.pt'),
)


@api_view(['GET'])
def health_status(request):
    """Lightweight endpoint used by the frontend/test script to verify the API is alive."""
    return Response({'ok': True, 'service': 'Check MyCure API'})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"].strip()
        email = serializer.validated_data["email"].strip().lower()
        password = serializer.validated_data["password"]
        gender = serializer.validated_data.get("gender", "")

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        Profile.objects.create(user=user, full_name=name, gender=gender)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {"id": user.id, "email": user.email, "name": name, "gender": gender},
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip().lower()
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        name = getattr(getattr(user, "profile", None), "full_name", "")

        return Response({"token": token.key, "user": {"id": user.id, "email": user.email, "name": name}})


class PredictView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        symptoms = request.data.get("symptoms", [])
        if not isinstance(symptoms, list):
            return Response({"error": "symptoms must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        result = predict_from_symptoms(symptoms)

        # Optional persistence if user is authenticated via token
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            SymptomCheck.objects.create(
                user=user,
                symptoms=symptoms,
                age=request.data.get("age") or None,
                gender=request.data.get("gender", "") or "",
                medical_history=request.data.get("history", "") or request.data.get("medical_history", "") or "",
                prediction=result.get("prediction", ""),
                confidence=result.get("confidence"),
            )

        return Response(result)


class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from .chatbot_service import generate_chatbot_response

        message = request.data.get("message")
        language = request.data.get("language", "en")
        result = generate_chatbot_response(message, language)
        if not (message or "").strip():
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


class SymptomCheckViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SymptomCheckSerializer

    def get_queryset(self):
        return SymptomCheck.objects.filter(user=self.request.user)


# Eye Detection Views
DISEASE_RECOMMENDATIONS = {
    'cataract': {
        'severity': 'moderate',
        'disease_info': 'A cataract is a clouding of the eye\'s lens that affects vision. It develops slowly and can occur in one or both eyes.',
        'symptoms': ['Cloudy or blurry vision', 'Faded colors', 'Glare sensitivity', 'Poor night vision', 'Double vision', 'Frequent prescription changes'],
        'causes': ['Aging', 'Diabetes', 'Eye injury', 'Prolonged steroid use', 'Excessive UV exposure', 'Smoking'],
        'treatment': 'Cataract surgery is the only effective treatment. The cloudy lens is removed and replaced with an artificial lens.',
        'prevention': ['Wear UV-blocking sunglasses', 'Quit smoking', 'Control diabetes', 'Regular eye exams', 'Eat antioxidant-rich foods'],
        'recommendations': '''👁️ CATARACT DETECTED\n\n📖 What is it?\nA cataract is clouding of the eye\'s natural lens, causing blurry vision like looking through a foggy window.\n\n⚠️ Immediate Actions:\n1. 👨‍⚕️ Schedule appointment with ophthalmologist within 1-2 weeks\n2. 🕶️ Wear UV-blocking sunglasses outdoors\n3. 💡 Ensure good lighting at home\n4. 🚗 Avoid driving at night if vision is impaired\n\n💊 Treatment Options:\n• Surgery: Phacoemulsification (lens replacement)\n• Success rate: >98%\n• Recovery time: 2-4 weeks\n• Usually outpatient procedure\n\n🍽️ Dietary Support:\n• Vitamin C & E rich foods\n• Leafy greens (spinach, kale)\n• Omega-3 fatty acids\n• Carrots, sweet potatoes\n\n✅ What to Expect:\n• Early stage: Stronger glasses may help\n• Advanced: Surgery is safe and effective\n• Post-surgery: Dramatic vision improvement\n\n📞 Emergency Signs (Call doctor):\n• Sudden vision loss\n• Severe eye pain\n• Seeing flashes of light\n• New floaters'''
    },
    'diabetic_retinopathy': {
        'severity': 'severe',
        'disease_info': 'Diabetic retinopathy is damage to blood vessels in the retina caused by high blood sugar. It\'s a leading cause of blindness in diabetic patients.',
        'symptoms': ['Blurred vision', 'Floaters', 'Dark spots', 'Vision loss', 'Difficulty seeing at night', 'Color perception changes'],
        'causes': ['Uncontrolled diabetes', 'High blood pressure', 'High cholesterol', 'Long diabetes duration', 'Pregnancy', 'Smoking'],
        'treatment': 'Laser treatment (photocoagulation), anti-VEGF injections, vitrectomy surgery, strict blood sugar control.',
        'prevention': ['Control blood sugar levels', 'Manage blood pressure', 'Regular dilated eye exams', 'Maintain healthy weight', 'Exercise regularly'],
        'recommendations': '''👁️ DIABETIC RETINOPATHY DETECTED\n\n📖 Critical Information:\nDiabetic retinopathy damages blood vessels in the retina due to high blood sugar. This is SERIOUS and requires immediate medical attention.\n\n🚨 URGENT - ACT NOW:\n1. 👨‍⚕️ See retina specialist WITHIN 48 HOURS\n2. 📊 Check blood sugar immediately\n3. 💉 Do NOT skip insulin/medications\n4. 📝 Document any vision changes\n\n🩺 Severity Levels:\n• Non-proliferative (early): Microaneurysms\n• Proliferative (advanced): New blood vessel growth\n• Macular edema: Swelling in central vision\n\n💊 Treatment Options:\n1. Anti-VEGF Injections:\n   - Stops abnormal vessel growth\n   - Monthly injections initially\n   - Highly effective\n\n2. Laser Photocoagulation:\n   - Seals leaking vessels\n   - Prevents new vessel growth\n   - Outpatient procedure\n\n3. Vitrectomy:\n   - For severe cases\n   - Removes blood from eye\n   - Requires surgery\n\n🎯 Blood Sugar Management (CRITICAL):\n• Target HbA1c: <7%\n• Test glucose 4-6 times daily\n• Never skip medications\n• Keep glucose log\n\n💔 Blood Pressure Control:\n• Target: <140/90 mmHg\n• Take BP medications regularly\n• Reduce salt intake\n\n🍽️ Dietary Changes (Start Today):\n• Low glycemic index foods\n• Avoid refined sugars\n• Increase fiber intake\n• Omega-3 fatty acids\n• Dark leafy greens\n\n⏰ Follow-up Schedule:\n• Retina specialist: Every 2-3 months\n• Endocrinologist: Monthly\n• Primary care: Regular checkups\n\n⚠️ WARNING SIGNS (Call 911):\n• Sudden complete vision loss\n• Severe eye pain\n• Sudden increase in floaters\n• Curtain over vision\n\n📚 Patient Support:\n• Diabetes educator consultation\n• Support groups\n• Low vision rehabilitation\n\n✍️ Your Action Plan:\n[ ] Schedule retina specialist appointment\n[ ] Check blood sugar now\n[ ] Review medications with doctor\n[ ] Start blood sugar log\n[ ] Make dietary changes\n[ ] Measure blood pressure daily'''
    },
    'glaucoma': {
        'severity': 'severe',
        'disease_info': 'Glaucoma is increased eye pressure damaging the optic nerve. Often called "silent thief of sight" as it causes gradual vision loss without symptoms.',
        'symptoms': ['Peripheral vision loss', 'Tunnel vision', 'Severe headache', 'Eye pain', 'Nausea', 'Blurred vision', 'Halos around lights'],
        'causes': ['High eye pressure', 'Family history', 'Age over 60', 'Thin corneas', 'Diabetes', 'High blood pressure'],
        'treatment': 'Eye drops, laser trabeculoplasty, drainage surgery, minimally invasive glaucoma surgery (MIGS).',
        'prevention': ['Regular eye pressure checks', 'Exercise regularly', 'Protect eyes from injury', 'Take eye drops as prescribed', 'Regular dilated exams'],
        'recommendations': '''👁️ GLAUCOMA DETECTED\n\n📖 Understanding Glaucoma:\nGlaucoma damages the optic nerve due to elevated eye pressure. It\'s called the "silent thief of sight" because vision loss is gradual and irreversible.\n\n🚨 EMERGENCY - IMMEDIATE ACTION REQUIRED:\n1. 👨‍⚕️ Contact ophthalmologist TODAY\n2. 🕒 Do NOT delay - every hour counts\n3. 📞 If acute: Call emergency services (severe pain, nausea, blurred vision)\n4. 📊 Get eye pressure measured ASAP\n\n🔴 Types of Glaucoma:\n\n1. Open-Angle (Most Common):\n   • Gradual vision loss\n   • No early symptoms\n   • Peripheral vision affected first\n   • Both eyes usually affected\n\n2. Angle-Closure (Emergency):\n   • Sudden severe symptoms\n   • Eye pain, headache\n   • Nausea and vomiting\n   • Requires immediate treatment\n\n💊 Treatment Protocol:\n\n1. Eye Drops (First Line):\n   • Prostaglandin analogs (Latanoprost)\n   • Beta-blockers (Timolol)\n   • Alpha agonists\n   • Carbonic anhydrase inhibitors\n   ⚠️ NEVER skip doses!\n\n2. Laser Treatment:\n   • Selective Laser Trabeculoplasty (SLT)\n   • Laser Peripheral Iridotomy (LPI)\n   • Outpatient procedure\n   • 15-30 minutes\n\n3. Surgery (If Needed):\n   • Trabeculectomy\n   • Drainage tube implant\n   • MIGS (minimally invasive)\n\n🎯 Target Eye Pressure:\n• Normal: 12-22 mmHg\n• Glaucoma target: Usually <18 mmHg\n• Varies per individual\n• Monitor regularly\n\n📅 Monitoring Schedule:\n• First year: Every 2-3 months\n• Stable: Every 4-6 months\n• Visual field tests: Annually\n• OCT scans: As recommended\n\n💪 Lifestyle Modifications:\n• Regular aerobic exercise (lowers pressure)\n• Avoid heavy lifting/straining\n• Sleep with head elevated\n• Reduce caffeine intake\n• Stay hydrated (sip water throughout day)\n• Avoid tight neckties/collars\n\n🍽️ Nutrition Support:\n• Leafy greens (nitric oxide)\n• Omega-3 fatty acids\n• Vitamins A, C, E\n• Zinc, copper\n• Antioxidant-rich foods\n\n⚠️ Medication Compliance:\n• Set daily alarms\n• Keep drops accessible\n• Proper drop technique\n• Wait 5 min between different drops\n• Close eyes 2 min after drops\n\n🚫 Activities to Avoid:\n• Inverted yoga positions\n• Heavy weight lifting\n• Playing wind instruments\n• Scuba diving (consult doctor)\n\n🚨 Emergency Warning Signs:\n• Sudden severe eye pain\n• Sudden vision loss\n• Seeing halos around lights\n• Severe headache with nausea\n• Red eye with cloudy cornea\n➜ CALL 911 IMMEDIATELY\n\n📝 Your Care Plan:\n[ ] Emergency ophthalmology appointment\n[ ] Start prescribed eye drops\n[ ] Set medication reminders\n[ ] Baseline visual field test\n[ ] OCT scan of optic nerve\n[ ] Inform family (hereditary risk)\n[ ] Get medical alert bracelet\n[ ] Join glaucoma support group\n\n📞 Important Numbers:\n• Ophthalmologist: ___________\n• Emergency eye care: ___________\n• Pharmacy: ___________\n\nℹ️ Remember:\n• Vision loss is permanent\n• Treatment slows/stops progression\n• Regular monitoring is ESSENTIAL\n• Never stop drops without doctor approval'''
    },
    'normal': {
        'severity': 'normal',
        'disease_info': 'Your eyes appear healthy with no signs of disease detected. Continue preventive care to maintain optimal eye health.',
        'symptoms': ['No abnormalities detected'],
        'causes': ['N/A - Healthy eyes'],
        'treatment': 'No treatment needed. Continue preventive care and regular checkups.',
        'prevention': ['Regular eye exams', 'UV protection', 'Healthy diet', 'Screen breaks', 'Stay hydrated', 'Don\'t smoke'],
        'recommendations': '''✅ HEALTHY EYES - EXCELLENT NEWS!\n\n🎉 Detection Results:\nNo signs of eye disease detected. Your eyes appear healthy and functioning normally.\n\n🚪 Preventive Care Plan:\n\n1. 📅 Regular Eye Exams:\n   • Age 20-39: Every 5-10 years\n   • Age 40-54: Every 2-4 years\n   • Age 55-64: Every 1-3 years\n   • Age 65+: Every 1-2 years\n   • With risk factors: Annually\n\n2. 🕶️ UV Protection:\n   • Wear 100% UV-blocking sunglasses\n   • Wide-brimmed hat outdoors\n   • Even on cloudy days\n   • Wrap-around styles best\n\n3. 💻 Digital Eye Care (20-20-20 Rule):\n   • Every 20 minutes\n   • Look 20 feet away\n   • For 20 seconds\n   • Blink frequently\n   • Adjust screen brightness\n   • Position screen 20-26 inches away\n\n4. 🍽️ Eye-Healthy Nutrition:\n   \n   Vitamin A (Night Vision):\n   • Carrots, sweet potatoes\n   • Spinach, kale\n   • Eggs, milk\n   \n   Vitamin C (Antioxidant):\n   • Oranges, strawberries\n   • Bell peppers\n   • Broccoli\n   \n   Vitamin E (Cell Protection):\n   • Almonds, sunflower seeds\n   • Avocados\n   \n   Omega-3 (Dry Eye Prevention):\n   • Salmon, tuna\n   • Walnuts, flaxseed\n   \n   Lutein & Zeaxanthin (Macular Health):\n   • Kale, spinach\n   • Corn, egg yolks\n   \n   Zinc (Overall Eye Health):\n   • Oysters, beef\n   • Pumpkin seeds\n\n5. 💧 Hydration:\n   • Drink 8-10 glasses water daily\n   • Prevents dry eyes\n   • Supports tear production\n   • Flush out toxins\n\n6. 🚫 Avoid Risk Factors:\n   • Don\'t smoke (doubles risk of AMD, cataracts)\n   • Limit alcohol\n   • Manage diabetes & blood pressure\n   • Maintain healthy weight\n   • Exercise regularly\n\n7. 👁️ Daily Eye Care:\n   • Remove eye makeup before bed\n   • Never sleep in contact lenses\n   • Clean contacts properly\n   • Replace contacts as directed\n   • Don\'t rub eyes excessively\n   • Keep hands clean\n\n8. 🏋️ Eye Exercises:\n   • Focus shifts (near/far)\n   • Eye rolls (clockwise/counter)\n   • Palming (warm palms on eyes)\n   • Figure 8 tracking\n   • Blinking exercises\n\n9. 😴 Sleep Quality:\n   • 7-9 hours nightly\n   • Dark, cool room\n   • Reduces eye strain\n   • Supports eye repair\n\n10. ⚗️ Eye Safety:\n    • Wear protective goggles for:\n      - Sports\n      - Yard work\n      - Power tools\n      - Swimming\n      - Chemical work\n\n🚨 When to See a Doctor (Don\'t Wait):\n• Sudden vision changes\n• Flashes of light\n• New floaters\n• Eye pain\n• Double vision\n• Persistent redness\n• Discharge\n• Light sensitivity\n\n📊 Track Your Eye Health:\n[ ] Schedule annual eye exam\n[ ] Update prescription if needed\n[ ] Buy UV-blocking sunglasses\n[ ] Set screen time reminders\n[ ] Add eye-healthy foods to diet\n[ ] Take omega-3 supplements\n[ ] Practice 20-20-20 rule\n[ ] Check family eye history\n\n🎯 Risk Factor Assessment:\nConsider more frequent exams if you have:\n• Family history of eye disease\n• Diabetes\n• High blood pressure\n• Previous eye injury/surgery\n• High myopia (nearsightedness)\n• Age over 40\n\n📚 Resources:\n• American Academy of Ophthalmology\n• Prevent Blindness America\n• National Eye Institute\n\n👏 Great Job!\nMaintaining healthy eyes is an ongoing commitment. Keep up these preventive measures to protect your vision for life!'''
    },
}

def get_recommendations(disease_name):
    disease_lower = disease_name.lower()
    for key in DISEASE_RECOMMENDATIONS:
        if key in disease_lower:
            return DISEASE_RECOMMENDATIONS[key]
    return {
        'severity': 'moderate',
        'recommendations': f'''🩺 {disease_name} Detected\n\n📋 Recommendations:\n1. Consult eye specialist\n2. Get comprehensive exam\n3. Follow prescribed treatment\n4. Regular monitoring\n5. Good eye hygiene\n\nSeek professional advice.'''
    }

@api_view(['POST'])
def detect_eye_disease(request):
    if not YOLO_AVAILABLE:
        return Response({'error': 'YOLO not available. Install: pip install ultralytics'}, status=500)
    
    try:
        image_data = None
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image = Image.open(image_file)
        elif 'image_base64' in request.data:
            image_base64 = request.data['image_base64']
            if 'base64,' in image_base64:
                image_base64 = image_base64.split('base64,')[1]
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
        else:
            return Response({'error': 'No image provided'}, status=400)
        
        img_array = np.array(image)
        if img_array.shape[-1] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        if not os.path.exists(MODEL_PATH):
            return Response({'error': f'Model not found at {MODEL_PATH}'}, status=500)
        
        model = YOLO(MODEL_PATH)
        results = model(img_array)
        
        detections = []
        best_detection = None
        max_confidence = 0
        
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                class_name = model.names[cls]
                detection = {'class': class_name, 'confidence': conf, 'box': box.xyxy[0].tolist()}
                detections.append(detection)
                if conf > max_confidence:
                    max_confidence = conf
                    best_detection = detection
        
        if best_detection and max_confidence > 0.3:
            disease = best_detection['class']
            confidence = max_confidence
        else:
            disease = 'normal'
            confidence = 0.95 if not detections else 0.5
        
        recommendations_data = get_recommendations(disease)
        
        annotated_img = results[0].plot()
        annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(annotated_img_rgb)
        img_buffer = io.BytesIO()
        pil_img.save(img_buffer, format='JPEG')
        processed_image_data = img_buffer.getvalue()
        
        user = request.user if request.user.is_authenticated else None
        
        eye_detection = EyeDetection.objects.create(
            user=user,
            disease=disease,
            confidence=confidence,
            detections={'results': detections},
            severity=recommendations_data['severity'],
            recommendations=recommendations_data['recommendations'],
            disease_info=recommendations_data.get('disease_info', ''),
            symptoms=recommendations_data.get('symptoms', []),
            causes=recommendations_data.get('causes', []),
            treatment=recommendations_data.get('treatment', ''),
            prevention=recommendations_data.get('prevention', [])
        )
        
        if 'image' in request.FILES:
            eye_detection.original_image.save(f'eye_scan_{eye_detection.id}.jpg', request.FILES['image'], save=True)
        elif image_data:
            eye_detection.original_image.save(f'eye_scan_{eye_detection.id}.jpg', ContentFile(image_data), save=True)
        
        eye_detection.processed_image.save(f'eye_scan_processed_{eye_detection.id}.jpg', ContentFile(processed_image_data), save=True)
        
        processed_base64 = base64.b64encode(processed_image_data).decode('utf-8')
        
        return Response({
            'success': True,
            'detection_id': eye_detection.id,
            'disease': disease,
            'confidence': round(confidence * 100, 2),
            'severity': recommendations_data['severity'],
            'recommendations': recommendations_data['recommendations'],
            'detections': detections,
            'processed_image': f'data:image/jpeg;base64,{processed_base64}'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_eye_detection_history(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    detections = EyeDetection.objects.filter(user=request.user)
    data = [{
        'id': det.id,
        'disease': det.disease,
        'confidence': det.confidence,
        'severity': det.severity,
        'recommendations': det.recommendations,
        'created_at': det.created_at,
        'original_image': request.build_absolute_uri(det.original_image.url) if det.original_image else None,
        'processed_image': request.build_absolute_uri(det.processed_image.url) if det.processed_image else None,
    } for det in detections]
    
    return Response(data)

EYE_RASA_URL = os.environ.get('RASA_EYE_URL', 'http://127.0.0.1:5005/webhooks/rest/webhook')

EYE_CHAT_FALLBACKS = {
    'red': 'Eye redness can have several causes, including irritation, dryness, allergy, or infection. If redness is severe, painful, persistent, or affects vision, please seek professional eye care.',
    'pain': 'Eye pain deserves attention. Severe pain, sudden vision changes, light sensitivity, nausea, or an eye injury are warning signs that need urgent professional assessment.',
    'blur': 'Blurred vision can have many causes. Sudden or severe changes in vision should be assessed urgently by an eye-care professional.',
    'dry': 'Dry eyes may feel burning, gritty, or watery. Take screen breaks and avoid direct air flow; persistent symptoms should be checked by an eye-care professional.',
    'itch': 'Itchy eyes are often associated with irritation or allergy. Avoid rubbing your eyes and seek professional advice if symptoms persist or there is pain or discharge.',
    'result': 'I can explain the eye screening result shown on this page. An image-based screening result is not a confirmed medical diagnosis.',
    'prevent': 'For eye health, use suitable UV protection, take regular screen breaks, avoid rubbing your eyes, protect your eyes during risky activities, and attend recommended eye examinations.',
}


def _local_eye_chat(message):
    text = (message or '').lower().strip()
    emergency_terms = ['sudden vision loss', 'cannot see', 'can\'t see', 'curtain over', 'severe eye pain', 'eye injury', 'sudden flashes', 'many new floaters']
    if any(term in text for term in emergency_terms):
        return {'intent': 'emergency_eye', 'text': 'This may be an eye emergency. Sudden vision loss, severe eye pain, major eye injury, or a curtain-like shadow over vision needs urgent medical attention.'}
    if not text:
        return {'intent': 'fallback', 'text': 'Tell me what you are noticing, such as redness, pain, dryness, itching, or blurred vision.'}
    if any(x in text for x in ['red', 'reddish', 'bloodshot', 'laal']): key, intent = 'red', 'eye_redness'
    elif any(x in text for x in ['hurt', 'hurting', 'pain', 'dard', 'dukh']): key, intent = 'pain', 'eye_pain'
    elif any(x in text for x in ['blur', 'blurry', 'dhundhli', 'not clear']): key, intent = 'blur', 'blurred_vision'
    elif any(x in text for x in ['dry', 'dryness', 'burning', 'gritty']): key, intent = 'dry', 'dry_eyes'
    elif any(x in text for x in ['itch', 'itchy', 'khujli']): key, intent = 'itch', 'itchy_eyes'
    elif any(x in text for x in ['result', 'report', 'scan', 'screening']): key, intent = 'result', 'eye_screening_result'
    elif any(x in text for x in ['prevent', 'protect', 'care', 'healthy eyes']): key, intent = 'prevent', 'prevention'
    else: return {'intent': 'fallback', 'text': 'I can help with common eye-health questions and screening results. Tell me what you are noticing, for example redness, pain, dryness, itching, or blurred vision.'}
    return {'intent': intent, 'text': EYE_CHAT_FALLBACKS[key]}


@api_view(['POST'])
def eye_chat(request):
    """Send an eye-health question to the optional Rasa assistant with a safe local fallback."""
    message = str(request.data.get('message', '')).strip()
    if not message:
        return Response({'error': 'message is required'}, status=400)
    try:
        rasa_response = requests.post(EYE_RASA_URL, json={'sender': 'checkmycure-eye', 'message': message}, timeout=4)
        rasa_response.raise_for_status()
        items = rasa_response.json()
        if isinstance(items, list) and items:
            texts = [str(item.get('text', '')).strip() for item in items if item.get('text')]
            if texts:
                return Response({'success': True, 'source': 'rasa', 'intent': 'rasa', 'text': '\n'.join(texts)})
    except (requests.RequestException, ValueError, TypeError):
        pass
    except Exception:
        # Keep the optional Rasa integration non-blocking if the local service is unavailable.
        pass
    fallback = _local_eye_chat(message)
    fallback['success'] = True
    fallback['source'] = 'local_fallback'
    return Response(fallback)


@api_view(['GET'])
def geocode_place(request):
    """Geocode a city/address through Nominatim from the server side."""
    query = (request.query_params.get('q') or '').strip()
    if not query:
        return Response({'error': 'q is required'}, status=400)
    headers = {'User-Agent': 'CheckMyCure/1.0 (local educational project)', 'Accept-Language': 'en'}
    for endpoint in [
        'https://nominatim.openstreetmap.org/search',
        'https://nominatim.openstreetmap.fr/search',
    ]:
        try:
            r = requests.get(endpoint, params={'format': 'jsonv2', 'q': query, 'limit': 1},
                             headers=headers, timeout=12)
            r.raise_for_status()
            data = r.json()
            if data:
                item = data[0]
                return Response({'lat': float(item['lat']), 'lng': float(item['lon']),
                                 'display_name': item.get('display_name', query)})
        except (requests.RequestException, ValueError):
            continue
    return Response({'error': 'Location service is temporarily unavailable or the location was not found'}, status=502)


@api_view(['GET'])
def nearby_clinics(request):
    """Find nearby clinics, hospitals and doctors through OpenStreetMap Overpass."""
    try:
        raw_lat = request.query_params.get('lat')
        raw_lng = request.query_params.get('lng')
        if raw_lat is None or raw_lng is None:
            raise ValueError
        lat = float(raw_lat)
        lng = float(raw_lng)
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            raise ValueError
    except (TypeError, ValueError):
        return Response({'error': 'lat must be between -90 and 90 and lng between -180 and 180'}, status=400)
    try:
        radius = min(max(int(request.query_params.get('radius', 5000)), 1000), 10000)
    except ValueError:
        radius = 5000
    query = f"""[out:json][timeout:25];
(
  nwr[\"amenity\"=\"clinic\"](around:{radius},{lat},{lng});
  nwr[\"amenity\"=\"hospital\"](around:{radius},{lat},{lng});
  nwr[\"amenity\"=\"doctors\"](around:{radius},{lat},{lng});
);
out center tags;"""
    try:
        r = requests.post('https://overpass-api.de/api/interpreter', data=query,
                          headers={'User-Agent': 'CheckMyCure/1.0 (health-app)'}, timeout=35)
        r.raise_for_status()
        places = []
        for e in r.json().get('elements', []):
            tags = e.get('tags', {})
            center = e.get('center') or {}
            elat = e.get('lat', center.get('lat'))
            elng = e.get('lon', center.get('lon'))
            if elat is None or elng is None:
                continue
            places.append({
                'name': tags.get('name') or 'Unnamed healthcare facility',
                'lat': float(elat), 'lng': float(elng),
                'type': tags.get('amenity', 'clinic'),
                'phone': tags.get('phone') or tags.get('contact:phone') or '',
                'address': ', '.join(x for x in [tags.get('addr:housenumber'), tags.get('addr:street'), tags.get('addr:city')] if x),
            })
        return Response({'results': places[:50]})
    except requests.RequestException as exc:
        return Response({'error': f'Nearby clinic service unavailable: {exc}'}, status=502)
