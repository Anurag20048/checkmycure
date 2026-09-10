function appendMessage(text, sender) {
    const chatBox = document.getElementById("chat-messages");
    if (!chatBox) return;

    // Skip showing error messages about Rasa
    if (text && text.toLowerCase().includes('rasa')) return;

    const msg = document.createElement("div");
    msg.className = sender === "user" ? "chat-user" : "chat-bot";
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("chat-input");
    if (!input || !input.value.trim()) return;

    const message = input.value.trim();
    input.value = "";

    appendMessage(message, "user");

    // Show typing indicator
    const chatBox = document.getElementById("chat-messages");
    const typingDiv = document.createElement("div");
    typingDiv.className = "bot typing-indicator";
    typingDiv.id = "typing-indicator";
    typingDiv.innerText = "Typing...";
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Try Django backend API first
    fetch('/api/chatbot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, language: 'en' })
    })
    .then(r => {
        if (!r.ok) throw new Error('Backend error');
        return r.json();
    })
    .then(data => {
        document.getElementById('typing-indicator')?.remove();
        appendMessage(data.response || generateChatbotResponse(message.toLowerCase()), "bot");
    })
    .catch(err => {
        console.log('Backend unavailable, using local chatbot');
        document.getElementById('typing-indicator')?.remove();
        const response = generateChatbotResponse(message.toLowerCase());
        appendMessage(response, "bot");
    });
}

// Smart chatbot response generator
function generateChatbotResponse(message) {
    // Greeting
    if (message.match(/\b(hi|hello|hey|good morning|good evening)\b/i)) {
        return "👋 Hello! I'm your health assistant. How can I help you today?";
    }
    
    // Fever symptoms
    if (message.match(/\b(fever|temperature|hot|burning up)\b/i)) {
        return "🤒 If you have a fever:\n\n1. Rest and drink plenty of fluids\n2. Take fever-reducing medication (paracetamol/ibuprofen)\n3. Monitor temperature regularly\n4. If fever persists >3 days or goes above 103°F (39.4°C), see a doctor\n\nIs there anything else bothering you?";
    }
    
    // Headache
    if (message.match(/\b(headache|head pain|migraine)\b/i)) {
        return "🧠 For headaches:\n\n1. Rest in a quiet, dark room\n2. Stay hydrated\n3. Apply cold/warm compress\n4. Take pain reliever if needed\n5. Avoid screens and bright lights\n\nIf severe or persistent, consult a doctor.";
    }
    
    // Cough
    if (message.match(/\b(cough|coughing|throat)\b/i)) {
        return "🤧 For cough relief:\n\n1. Drink warm liquids (tea, honey water)\n2. Use cough drops or lozenges\n3. Use a humidifier\n4. Avoid irritants (smoke, dust)\n5. Elevate your head while sleeping\n\nSee a doctor if cough lasts >2 weeks or has blood.";
    }
    
    // Cold/Flu
    if (message.match(/\b(cold|flu|runny nose|sneezing)\b/i)) {
        return "🤧 Common cold/flu care:\n\n1. Rest well\n2. Drink lots of fluids\n3. Gargle with salt water\n4. Take vitamin C\n5. Use saline nasal drops\n6. Keep warm\n\nMost colds resolve in 7-10 days.";
    }
    
    // Stomach issues
    if (message.match(/\b(stomach|nausea|vomit|diarrhea|abdominal pain)\b/i)) {
        return "🤢 For digestive issues:\n\n1. Eat bland foods (rice, bananas, toast)\n2. Stay hydrated with ORS\n3. Avoid spicy/oily foods\n4. Rest your stomach\n5. Take antacids if needed\n\nSeek medical help if severe pain or blood in stool.";
    }
    
    // Chest pain - EMERGENCY
    if (message.match(/\b(chest pain|heart pain|cardiac)\b/i)) {
        return "🚨 CHEST PAIN IS SERIOUS!\n\n⚠️ If you're experiencing chest pain, especially with:\n- Shortness of breath\n- Pain radiating to arm/jaw\n- Sweating\n- Nausea\n\n📞 CALL EMERGENCY (112) IMMEDIATELY or go to nearest hospital!\n\nDo you need emergency services?";
    }
    
    // Breathing problems - EMERGENCY
    if (message.match(/\b(can't breathe|breathing difficulty|suffocating|choking)\b/i)) {
        return "🚨 BREATHING DIFFICULTY - EMERGENCY!\n\n📞 CALL 112 IMMEDIATELY!\n\nWhile waiting:\n1. Sit upright\n2. Loosen tight clothing\n3. Try slow, deep breaths\n4. Stay calm\n\nDo you need me to call emergency services?";
    }
    
    // COVID symptoms
    if (message.match(/\b(covid|coronavirus|loss of taste|loss of smell)\b/i)) {
        return "🦠 COVID-19 related:\n\n1. Get tested if you suspect COVID\n2. Isolate from others\n3. Monitor symptoms\n4. Rest and hydrate\n5. Track oxygen levels if possible\n\nSeek immediate care if:\n- Difficulty breathing\n- Chest pain\n- Confusion\n- Blue lips/face";
    }
    
    // Diabetes
    if (message.match(/\b(diabetes|sugar|blood sugar|insulin)\b/i)) {
        return "🩸 Diabetes management:\n\n1. Monitor blood sugar regularly\n2. Follow prescribed medication\n3. Eat balanced meals\n4. Exercise regularly\n5. Stay hydrated\n6. Foot care is important\n\nConsult your doctor for personalized advice.";
    }
    
    // Blood pressure
    if (message.match(/\b(blood pressure|hypertension|bp|high pressure)\b/i)) {
        return "🩺 Blood pressure tips:\n\n1. Reduce salt intake\n2. Exercise regularly\n3. Maintain healthy weight\n4. Limit alcohol\n5. Manage stress\n6. Take medications as prescribed\n\nMonitor BP regularly and see your doctor.";
    }
    
    // Mental health
    if (message.match(/\b(anxiety|depression|stress|mental health|panic|worry)\b/i)) {
        return "🧘 Mental health support:\n\n1. Talk to someone you trust\n2. Practice deep breathing\n3. Exercise regularly\n4. Maintain sleep schedule\n5. Limit caffeine/alcohol\n6. Consider professional help\n\n📞 Mental health helpline: 1800-599-0019\n\nYou're not alone. It's okay to seek help.";
    }
    
    // Allergies
    if (message.match(/\b(allergy|allergies|allergic|rash|itching|skin rash)\b/i)) {
        return "🤧 Allergy management:\n\n1. Identify and avoid triggers\n2. Take antihistamines\n3. Use prescribed inhalers if needed\n4. Keep emergency medication handy\n5. Wear medical alert bracelet\n\nSeek immediate help for severe reactions (anaphylaxis).";
    }
    
    // Fatigue
    if (message.match(/\b(fatigue|tired|exhausted|weakness|weak)\b/i)) {
        return "😴 Dealing with fatigue:\n\n1. Get adequate sleep (7-9 hours)\n2. Stay hydrated\n3. Eat balanced meals\n4. Exercise regularly\n5. Manage stress\n6. Check for anemia or vitamin deficiency\n\nPersistent fatigue may need medical evaluation.";
    }
    
    // Dizziness
    if (message.match(/\b(dizzy|dizziness|vertigo|lightheaded)\b/i)) {
        return "🌀 For dizziness:\n\n1. Sit or lie down immediately\n2. Stay hydrated\n3. Avoid sudden movements\n4. Check blood pressure\n5. Avoid driving\n\nSeek help if with chest pain, fainting, or severe headache.";
    }
    
    // Back Pain
    if (message.match(/\b(back pain|backache|spine pain)\b/i)) {
        return "🦴 Back pain relief:\n\n1. Apply hot/cold compress\n2. Gentle stretching\n3. Maintain good posture\n4. Avoid heavy lifting\n5. Use supportive mattress\n6. Take pain relievers if needed\n\nSee doctor if pain persists >2 weeks or has numbness.";
    }
    
    // Joint Pain
    if (message.match(/\b(joint pain|arthritis|knee pain|elbow pain)\b/i)) {
        return "🦵 Joint pain management:\n\n1. Rest the joint\n2. Apply ice/heat\n3. Gentle exercises\n4. Maintain healthy weight\n5. Take anti-inflammatory medication\n6. Use joint support if needed\n\nConsult doctor for persistent or worsening pain.";
    }
    
    // Ear Pain
    if (message.match(/\b(ear pain|earache|ear infection)\b/i)) {
        return "👂 Ear pain care:\n\n1. Apply warm compress\n2. Don't insert anything in ear\n3. Take pain relievers\n4. Stay hydrated\n5. Avoid flying if possible\n\nSee doctor if severe pain, fever, or hearing loss.";
    }
    
    // Eye Pain
    if (message.match(/\b(eye pain|eye strain|red eyes)\b/i)) {
        return "👁️ Eye care:\n\n1. Rest your eyes\n2. Apply cool compress\n3. Use artificial tears\n4. Reduce screen time\n5. Ensure good lighting\n6. Remove contact lenses\n\nSeek immediate care for sudden vision changes.";
    }
    
    // Toothache
    if (message.match(/\b(toothache|tooth pain|dental pain)\b/i)) {
        return "🦷 Toothache relief:\n\n1. Rinse with warm salt water\n2. Use dental floss gently\n3. Take pain relievers\n4. Apply cold compress outside\n5. Avoid hot/cold foods\n\nSee a dentist as soon as possible.";
    }
    
    // Insomnia
    if (message.match(/\b(insomnia|can't sleep|sleepless|sleep problem)\b/i)) {
        return "😵 Better sleep tips:\n\n1. Maintain regular sleep schedule\n2. Create dark, cool bedroom\n3. Avoid screens before bed\n4. Limit caffeine/alcohol\n5. Try relaxation techniques\n6. Exercise during day\n\nConsult doctor if insomnia persists >3 weeks.";
    }
    
    // Constipation
    if (message.match(/\b(constipation|constipated|bowel movement)\b/i)) {
        return "🚽 Constipation relief:\n\n1. Drink more water\n2. Eat high-fiber foods\n3. Exercise regularly\n4. Don't ignore urge\n5. Consider stool softener\n6. Avoid processed foods\n\nSee doctor if severe or lasting >2 weeks.";
    }
    
    // Weight Loss
    if (message.match(/\b(weight loss|losing weight|thin)\b/i)) {
        return "⚖️ Unintentional weight loss:\n\n⚠️ If losing weight without trying, see a doctor as it may indicate:\n- Thyroid problems\n- Diabetes\n- Depression\n- Digestive issues\n- Other conditions\n\nFor healthy weight loss, consult nutritionist.";
    }
    
    // Women's Health
    if (message.match(/\b(irregular periods|menstrual|period pain|cramps)\b/i)) {
        return "📅 Menstrual health:\n\nFor period pain:\n1. Apply heating pad\n2. Take pain relievers\n3. Light exercise\n4. Stay hydrated\n\nIrregular periods may be due to:\n- Stress\n- PCOS\n- Thyroid issues\n\nConsult gynecologist if concerned.";
    }
    
    // Medication questions
    if (message.match(/\b(medicine|medication|drug|prescription|tablet|pill)\b/i)) {
        return "💊 Medication advice:\n\n⚠️ I cannot prescribe medications. Please:\n\n1. Consult a doctor or pharmacist\n2. Never share prescriptions\n3. Complete full course\n4. Check for interactions\n5. Follow dosage instructions\n\nDo you need to find a nearby clinic?";
    }
    
    // Doctor/Hospital
    if (message.match(/\b(doctor|hospital|clinic|appointment)\b/i)) {
        return "🏯 Finding medical care:\n\nI can help you find:\n1. 🏭 Nearby hospitals\n2. 👨‍⚕️ General practitioners\n3. 💊 Pharmacies\n\nWould you like me to show nearby healthcare facilities?";
    }
    
    // Emergency
    if (message.match(/\b(emergency|urgent|critical|help me|dying)\b/i)) {
        return "🚨 EMERGENCY ASSISTANCE\n\n📞 Call 112 (Emergency) immediately!\n\ud83d� Or use our SOS button in the app\n\nEmergency signs:\n- Severe chest pain\n- Difficulty breathing\n- Heavy bleeding\n- Loss of consciousness\n- Severe allergic reaction\n\nDon't wait - seek immediate help!";
    }
    
    // Thanks
    if (message.match(/\b(thank|thanks|appreciate)\b/i)) {
        return "🙏 You're welcome! Remember, I'm here to help. Stay healthy and take care! 💚";
    }
    
    // Bye
    if (message.match(/\b(bye|goodbye|see you)\b/i)) {
        return "👋 Take care! Feel free to come back anytime you need health advice. Stay safe! 💚";
    }
    
    // Default response
    return "🤖 I can help you with:\n\n• Symptom checking\n• General health advice\n• Finding nearby hospitals\n• Emergency guidance\n• Medication information\n\nTry asking about specific symptoms like 'fever', 'headache', or 'stomach pain'.";
}

// Rasa is disabled - using Django backend chatbot API instead
// const RASA_URL = "http://localhost:5005/webhooks/rest/webhook";
let rasaAvailable = false; // Always use Django backend

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("symptoms")) {
        flowState.step = 1;
        goToStep(1);
    }
});

let typingTimer = null;
let lastTypingHint = "";
let lastDetectedEmotion = null;
let emergencyMode = false;

document.getElementById("chat-input")?.addEventListener("input", (e) => {
    clearTimeout(typingTimer);
    const text = e.target.value.toLowerCase();

    typingTimer = setTimeout(() => {

        const symptomHints = [
            "fever", "cough", "headache", "nausea",
            "chest pain", "dizzy", "weak", "vomit"
        ];

        const detected = symptomHints.find(s => text.includes(s));

        if (detected && detected !== lastTypingHint) {
            lastTypingHint = detected;
            appendMessage(`👀 I noticed "${detected}". Tell me more.`, "bot");
        }

    }, 600); // reacts in < 1 second

    const emotion = detectEmotion(text);

    if (emotion && emotion !== lastDetectedEmotion) {
        lastDetectedEmotion = emotion;

        const empathyMessages = {
            anxious: "💙 I understand this can be worrying. I’m here to help.",
            panic: "🫂 Please pause and take a slow breath. I’m here with you.",
            stressed: "🌱 It sounds stressful. Let’s take this step by step."
        };

        appendMessage(empathyMessages[emotion], "bot");
    }

});

const symptomCategories = {
    general: [
        "Fever",
        "Fatigue",
        "Weight loss",
        "Loss of appetite",
        "Chills",
        "Weakness",
        "Body aches",
        "Sweating",
        "Dehydration",
        "Malaise"
    ],
    respiratory: [
        "Cough",
        "Shortness of breath",
        "Chest tightness",
        "Wheezing",
        "Sore throat",
        "Dry cough",
        "Productive cough",
        "Chest pain while breathing",
        "Rapid breathing",
        "Hoarseness"
    ],
    ent: [
        "Runny nose",
        "Nasal congestion",
        "Ear pain",
        "Hearing loss",
        "Sinus pressure",
        "Sneezing",
        "Ear discharge",
        "Loss of smell",
        "Loss of taste",
        "Throat irritation",
        "Swollen tonsils"
    ],
    gastro: [
        "Nausea",
        "Vomiting",
        "Diarrhea",
        "Abdominal pain",
        "Heartburn",
        "Constipation",
        "Stomach cramps",
        "Bloating",
        "Acid reflux",
        "Blood in stool",
        "Dark stools"
    ],
    neuro: [
        "Headache",
        "Dizziness",
        "Seizures",
        "Numbness",
        "Memory issues",
        "Lightheadedness",
        "Confusion",
        "Difficulty concentrating",
        "Fainting",
        "Tingling sensation",
        "Sensitivity to light"

    ],
    musculo: [
        "Joint pain",
        "Muscle pain",
        "Back pain",
        "Stiffness",
        "Swelling",
        "Muscle_stiffness",
        "Swollen joints",
        "Reduced mobility",
        "Neck stiffness",
        "Muscle cramps",
        "limb weakness",
        "sudden inability to move limb"
    ],
    cardio: [
        "Chest pain",
        "Palpitations",
        "Shortness of breath",
        "Dizziness",
        "Swelling in legs",
        "Rapid heartbeat",
        "Slow heartbeat",
        "Irregular heartbeat",
        "Chest pressure",
        "Cold extremities",
        "Sudden drop in blood pressure",
        "Faint pulse"
    ],
    urinary: [
        "Painful urination",
        "Frequent urination",
        "Blood in urine",
        "Lower abdominal pain",
        "Reduced urine output",
        "Dark urine",
        "Foul smelling urine",
        "Urinary urgency",
        "Difficulty urinating",
        "Flank pain"
    ]
};

let selectedSymptoms = [];
let flowState = { step: 1, age: null, gender: null, history: null };
let markersLayer = null;
let userLocation = null;
// ---------- AUTH HELPERS ----------
function isLoggedIn() {
    return localStorage.getItem("isLoggedIn") === "true";
}

function loginUser(name = "User") {
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("userName", name);
}

function logoutUser() {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("userName");
}

function showLoginRedirect() {
    // You can later replace with modal
    window.location.href = "login.html"; // or signup page
}

function goToLogin() {
    window.location.href = "login.html";
}

function updateHeaderUI() {
    const profileMenu = document.getElementById("profileMenu");
    const welcome = document.getElementById("welcomeMessage");

    if (!profileMenu) return;

    if (isLoggedIn()) {
        profileMenu.style.display = "block";
        if (welcome) {
            welcome.textContent = `Hi, ${localStorage.getItem("userName") || "User"}`;
        }
    } else {
        profileMenu.style.display = "none";
        if (welcome) welcome.textContent = "";
    }

    const logout = document.getElementById("logoutLink");
    if (logout) {
        logout.style.display = isLoggedIn() ? "block" : "none";
    }

    function updateRestrictedCards() {
        const clinicCard = document.querySelector(".card:nth-child(2)");
        const historyCard = document.querySelector(".card:nth-child(3)");

        if (!isLoggedIn()) {
            clinicCard?.classList.add("disabled-card");
            historyCard?.classList.add("disabled-card");
        } else {
            clinicCard?.classList.remove("disabled-card");
            historyCard?.classList.remove("disabled-card");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    updateHeaderUI();
    updateRestrictedCards();
});

const logoutLink = document.getElementById("logoutLink");

if (logoutLink) {
    logoutLink.addEventListener("click", () => {
        logoutUser();
        alert("Logged out successfully");
        window.location.href = "index.html";
    });
}

function updateUI() {
    const t = translations[currentLanguage];
    const logoTitle = document.querySelector('.logo-text');
    if (logoTitle) logoTitle.textContent = t.siteTitle;
    const navButtons = document.querySelectorAll('nav button');
    if (navButtons && navButtons.length >= 4) {
        navButtons[0].textContent = t.onboarding;
        navButtons[1].textContent = t.symptoms;
        navButtons[3].textContent = t.results;
    }
    // update hero/onboarding if present
    const heroHeading = document.querySelector('.hero-text h2');
    if (heroHeading) heroHeading.textContent = t.heroTitle || t.onboarding;
    const symptomsH2 = document.querySelector('#symptoms .page-title');
    if (symptomsH2) symptomsH2.textContent = t.symptoms;
    const resultsH2 = document.querySelector('#results h2'); if (resultsH2) resultsH2.textContent = t.results;
    const predictBtn = document.querySelector('#symptoms button'); if (predictBtn) predictBtn.textContent = t.predictIllness;
    const resultsBtn = document.querySelector('#results button'); if (resultsBtn) resultsBtn.textContent = t.findClinics;
    // update hero icon-row labels
    document.querySelectorAll('.icon-item[data-symptom]').forEach((el) => {
        const s = el.dataset.symptom;
        const span = el.querySelector('span');
        if (span && t[s]) span.textContent = t[s];
        if (el.classList.contains('add') && t.add) span.textContent = t.add;
        el.setAttribute('aria-pressed', selectedSymptoms.includes(s) ? 'true' : 'false');
    });

    document.querySelectorAll('.symptom').forEach((el, i) => {
        const symptoms = ['fever', 'cough', 'headache', 'nausea', 'fatigue', 'pain'];
        const sym = symptoms[i];
        el.innerHTML = `<i class="fas fa-${getIcon(sym)}"></i> ${t[sym]}`;
        el.setAttribute('data-symptom', sym);
        el.setAttribute('role', 'button');
        el.setAttribute('tabindex', '0');
        el.setAttribute('aria-pressed', selectedSymptoms.includes(sym) ? 'true' : 'false');
        el.onclick = () => selectSymptom(sym);
        el.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectSymptom(sym); } };
        if (selectedSymptoms.includes(sym)) el.classList.add('selected'); else el.classList.remove('selected');
    });

    // ensure event handlers are bound after UI update
    bindSymptomHandlers();

    // hero lead and CTA
    const lead = document.querySelector('.lead'); if (lead && t.lead) lead.textContent = t.lead;
    const ctas = document.querySelectorAll('.hero-cta button');
    if (ctas && ctas[0]) ctas[0].textContent = t.getStarted || 'Get started';
    if (ctas && ctas[1]) ctas[1].textContent = t.howItWorks || 'How it works';

    // feature cards
    const cards = document.querySelectorAll('.feature-cards .card');
    if (cards && cards.length >= 3) {
        const ft = [
            { title: 'feature1Title', desc: 'feature1Desc' },
            { title: 'feature2Title', desc: 'feature2Desc' },
            { title: 'feature3Title', desc: 'feature3Desc' }
        ];
        cards.forEach((c, idx) => {
            const h = c.querySelector('h3'); const p = c.querySelector('p');
            if (h) h.textContent = t[ft[idx].title] || h.textContent;
            if (p) p.textContent = t[ft[idx].desc] || p.textContent;
        });
    }
}

function getTrials() {
    return Number(localStorage.getItem("symptomTrials") || 0);
}

function incrementTrials() {
    let trials = getTrials() + 1;
    localStorage.setItem("symptomTrials", trials);
    return trials;
}

function bindSymptomHandlers() {
    // Bind icon items
    document.querySelectorAll('.icon-item[data-symptom]').forEach(el => {
        const s = el.dataset.symptom;
        if (!s) return;
        el.onclick = () => selectSymptom(s);
        el.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectSymptom(s); } };
        el.setAttribute('role', 'button');
        el.setAttribute('tabindex', '0');
    });
    // Bind grid symptom cards
    document.querySelectorAll('.symptom').forEach(el => {
        const s = el.dataset.symptom;
        if (!s) return;
        el.onclick = () => selectSymptom(s);
        el.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectSymptom(s); } };
    });
}

/* Flow (stepper) handling */
function nextStep() {
    const current = flowState.step;
    if (current === 1) {
        selectedSymptoms = readSelectedSymptomsFromDropdown();

        if (selectedSymptoms.length === 0) {
            alert("Please select at least one symptom.");
            return;
        }

        const trials = incrementTrials();

        if (trials > 3 && !isLoggedIn()) {
            alert("You have used all 3 free symptom checks. Please sign in.");
            showLoginRedirect();
            return;
        }
    }

    if (current === 2) {
        flowState.age = document.getElementById('age').value;
        // Try to get gender from radio buttons first, fallback to text input if exists
        const genderRadio = document.querySelector('input[name="gender"]:checked');
        flowState.gender = genderRadio ? genderRadio.value : (document.getElementById('gender') ? document.getElementById('gender').value : '');
        flowState.history = document.getElementById('history').value;

        // Get natural remedies for selected symptoms
        const naturalRemedies = getNaturalRemedies(selectedSymptoms);

        // Build remedies HTML
        let remediesHTML = '';
        if (naturalRemedies.length > 0) {
            remediesHTML = '<div class="natural-remedies-section"><h3>🌿 Natural Remedies for Your Symptoms</h3>';
            naturalRemedies.forEach(remedy => {
                remediesHTML += `
                    <div class="remedy-card">
                        <h4>${remedy.icon} ${remedy.symptom}</h4>
                        <ul class="remedy-list">
                            ${remedy.remedies.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            remediesHTML += '<p class="remedy-disclaimer">⚠️ These are complementary remedies. If symptoms persist or worsen, please consult a healthcare professional.</p></div>';
        }

        // populate review with patient info and remedies
        const review = document.getElementById('review');
        review.innerHTML = `
            <div class="review-info">
                <p><strong>Symptoms:</strong> ${selectedSymptoms.join(', ')}</p>
                <p><strong>Age:</strong> ${flowState.age || '—'}</p>
                <p><strong>Gender:</strong> ${flowState.gender || '—'}</p>
                <p><strong>History:</strong> ${flowState.history || '—'}</p>
            </div>
            ${remediesHTML}
        `;
    }
    goToStep(current + 1);
}

function openSymptomChecker() {
    const trials = getTrials();

    if (trials >= 3 && !isLoggedIn()) {
        alert("Please sign in to continue using the Symptom Checker.");
        showLoginRedirect();
        return;
    }

    showSection("symptoms");
}

function goToStep(n) {
    flowState.step = n;
    document.querySelectorAll('#stepper .step').forEach(s => s.classList.remove('active'));
    const stepEl = document.querySelector(`#stepper .step[data-step="${n}"]`);
    if (stepEl) stepEl.classList.add('active');
    document.querySelectorAll('.step-content').forEach(c => c.style.display = 'none');
    const content = document.querySelector(`.step-content[data-step="${n}"]`);
    if (content) content.style.display = 'block';
}

function getIcon(symptom) {
    const icons = { fever: 'thermometer-half', cough: 'lungs', headache: 'head-side-virus', nausea: 'dizzy', fatigue: 'tired', pain: 'band-aid' };
    return icons[symptom];
}

function getNaturalRemedies(symptoms) {
    const remediesDatabase = {
        fever: {
            icon: '🌡️',
            remedies: [
                'Drink plenty of water and herbal teas (chamomile, peppermint)',
                'Take a lukewarm bath to reduce body temperature',
                'Apply cool, damp washcloth to forehead',
                'Consume ginger tea with honey',
                'Eat light, easily digestible foods like soup',
                'Get adequate rest in a cool, comfortable room'
            ]
        },
        cough: {
            icon: '🫁',
            remedies: [
                'Drink warm honey and lemon tea (powerful natural cough suppressant)',
                'Inhale steam from hot water with eucalyptus oil',
                'Consume ginger tea or chew fresh ginger',
                'Gargle with salt water to soothe throat',
                'Stay hydrated with warm fluids',
                'Use a humidifier to add moisture to the air',
                'Drink turmeric milk before bed'
            ]
        },
        headache: {
            icon: '🧠',
            remedies: [
                'Drink plenty of water - dehydration is a common cause',
                'Apply cold or warm compress to forehead/neck',
                'Try peppermint or lavender essential oil on temples',
                'Drink ginger tea to reduce inflammation',
                'Practice deep breathing and meditation',
                'Massage your temples, neck, and shoulders',
                'Ensure adequate sleep and reduce screen time'
            ]
        },
        nausea: {
            icon: '🤢',
            remedies: [
                'Sip ginger tea or chew fresh ginger (highly effective)',
                'Try peppermint tea or smell peppermint oil',
                'Eat small, bland meals (crackers, toast, rice)',
                'Drink chamomile tea to calm stomach',
                'Consume lemon water or suck on lemon slices',
                'Avoid strong odors and fatty foods',
                'Practice slow, deep breathing exercises'
            ]
        },
        fatigue: {
            icon: '😴',
            remedies: [
                'Get 7-9 hours of quality sleep',
                'Drink green tea for natural energy boost',
                'Eat iron-rich foods (spinach, lentils, beans)',
                'Consume vitamin C-rich fruits (oranges, kiwi)',
                'Stay hydrated throughout the day',
                'Take short walks in fresh air and sunlight',
                'Eat small, frequent meals with protein',
                'Try ashwagandha or ginseng supplements (consult doctor first)'
            ]
        },
        pain: {
            icon: '🩹',
            remedies: [
                'Apply cold compress for acute pain/swelling',
                'Apply warm compress for chronic pain/stiffness',
                'Drink turmeric milk (golden milk) - natural anti-inflammatory',
                'Consume omega-3 rich foods (fish, walnuts, flaxseeds)',
                'Try gentle stretching and yoga',
                'Use arnica gel or oil for topical relief',
                'Drink ginger tea to reduce inflammation',
                'Practice meditation and relaxation techniques'
            ]
        }
    };

    let allRemedies = [];
    symptoms.forEach(symptom => {
        if (remediesDatabase[symptom]) {
            allRemedies.push({
                symptom: symptom.charAt(0).toUpperCase() + symptom.slice(1),
                icon: remediesDatabase[symptom].icon,
                remedies: remediesDatabase[symptom].remedies
            });
        }
    });

    return allRemedies;
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

function selectSymptom(symptom) {
    const element = document.querySelector(`.symptom[data-symptom="${symptom}"]`);
    if (!element) return;
    if (selectedSymptoms.includes(symptom)) {
        selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
        element.classList.remove('selected');
        element.setAttribute('aria-pressed', 'false');
    } else {
        selectedSymptoms.push(symptom);
        element.classList.add('selected');
        element.setAttribute('aria-pressed', 'true');
    }
}

// allow icon-row buttons to toggle selection too
document.addEventListener('click', (e) => {
    const btn = e.target.closest('.icon-item');
    if (btn && btn.dataset && btn.dataset.symptom) {
        selectSymptom(btn.dataset.symptom);
    }
    const sym = e.target.closest('.symptom');
    if (sym && sym.dataset && sym.dataset.symptom) {
        selectSymptom(sym.dataset.symptom);
    }
});

function predictIllness() {
    if (selectedSymptoms.length === 0) {
        alert('Please select at least one symptom.');
        return;
    }
    // Try backend prediction if available
    const payload = { symptoms: selectedSymptoms };
    fetch('/api/predict/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(r => {
        if (!r.ok) throw new Error('Backend error');
        return r.json();
    }).then(data => {
        const predEl = document.getElementById('prediction');
        const suggEl = document.getElementById('suggestions');
        const predParts = [];
        if (data.prediction) predParts.push(`<h3>Predicted: ${data.prediction}</h3>`);
        if (data.raw_prediction !== undefined) predParts.push(`<div>Raw: ${data.raw_prediction}</div>`);
        if (data.confidence !== undefined && data.confidence !== null) {
            const conf = (typeof data.confidence === 'number') ? (Math.round(data.confidence * 10000) / 100) + '%' : String(data.confidence);
            predParts.push(`<div>Confidence: ${conf}</div>`);
        }
        if (data.probabilities && typeof data.probabilities === 'object') {
            const rows = Object.keys(data.probabilities).map(k => `<li>${k}: ${Math.round(data.probabilities[k] * 10000) / 100}%</li>`).join('');
            predParts.push(`<div><strong>Probabilities:</strong><ul>${rows}</ul></div>`);
        }
        predEl.innerHTML = predParts.join('');
        suggEl.innerHTML = '<h3>Suggestions:</h3><ul><li>' + (data.suggestions || []).join('</li><li>') + '</li></ul>';
        document.getElementById("results").style.display = "block";
        document.getElementById("results").scrollIntoView({ behavior: "smooth" });
    }).catch(err => {
        console.warn('Backend unavailable; showing safe fallback', err);
        document.getElementById('prediction').innerHTML = '<h3>Unable to calculate a result</h3><p>The health prediction service is temporarily unavailable. Please try again when the server is running.</p>';
        document.getElementById('suggestions').innerHTML = '<h3>What to do:</h3><ul><li>Do not rely on an offline prediction.</li><li>If symptoms are severe or worsening, seek medical care.</li><li>Try again after reconnecting to the Check MyCure server.</li></ul>';
        document.getElementById("results").style.display = "block";
        document.getElementById("results").scrollIntoView({ behavior: "smooth" });

    });

    if (isLoggedIn()) {
        const history = JSON.parse(localStorage.getItem("healthHistory")) || [];
        history.push({
            date: new Date().toLocaleString(),
            symptoms: [...selectedSymptoms],
            prediction: prediction
        });
        localStorage.setItem("healthHistory", JSON.stringify(history));
    }

}

function openNearbyClinics() {
    if (!isLoggedIn()) {
        alert("Please sign in to access Nearby Clinics.");
        return;
    }
    showSection("clinics");
}

function openHistory() {
    if (!isLoggedIn()) {
        alert("Please sign in to view History & Records.");
        return;
    }
    window.location.href = "dashboard.html";
}

function predictDiseaseFromSymptoms(symptoms, originalMessage) {
    // Disease prediction database based on symptom combinations
    const diseaseDatabase = {
        'Common Cold': {
            symptoms: ['cough', 'headache', 'fatigue', 'fever'],
            confidence: 0.75,
            advice: 'Rest, drink plenty of fluids, and take over-the-counter cold medications. Usually resolves in 7-10 days.'
        },
        'Influenza (Flu)': {
            symptoms: ['fever', 'cough', 'fatigue', 'headache', 'pain'],
            confidence: 0.80,
            advice: 'Get plenty of rest, stay hydrated, and consider antiviral medication if caught early. Symptoms usually last 1-2 weeks.'
        },
        'Gastroenteritis (Stomach Flu)': {
            symptoms: ['nausea', 'vomit', 'stomach', 'fatigue'],
            confidence: 0.78,
            advice: 'Stay hydrated with small sips of water or electrolyte drinks. Eat bland foods when ready. Usually resolves in 1-3 days.'
        },
        'Migraine': {
            symptoms: ['headache', 'nausea', 'fatigue'],
            confidence: 0.72,
            advice: 'Rest in a quiet, dark room. Apply cold compress to forehead. Take prescribed migraine medication or over-the-counter pain relievers.'
        },
        'Tension Headache': {
            symptoms: ['headache', 'pain', 'fatigue'],
            confidence: 0.70,
            advice: 'Practice stress management, ensure good posture, and take over-the-counter pain relievers. Apply heat or cold to neck and shoulders.'
        },
        'Upper Respiratory Infection': {
            symptoms: ['cough', 'fever', 'fatigue', 'headache'],
            confidence: 0.76,
            advice: 'Rest, drink fluids, use a humidifier, and take over-the-counter medications for symptom relief. See a doctor if symptoms worsen.'
        },
        'Food Poisoning': {
            symptoms: ['nausea', 'vomit', 'stomach', 'fever'],
            confidence: 0.74,
            advice: 'Stay hydrated, rest, and avoid solid foods initially. Symptoms usually improve in 24-48 hours. Seek medical help if severe.'
        },
        'Viral Infection': {
            symptoms: ['fever', 'fatigue', 'headache', 'pain'],
            confidence: 0.68,
            advice: 'Rest, stay hydrated, and take over-the-counter medications for symptom relief. Most viral infections resolve on their own.'
        },
        'Chronic Fatigue Syndrome': {
            symptoms: ['fatigue', 'tired', 'headache', 'pain'],
            confidence: 0.65,
            advice: 'Consult a doctor for proper diagnosis. Management includes pacing activities, stress reduction, and symptom management.'
        },
        'COVID-19': {
            symptoms: ['fever', 'cough', 'fatigue', 'headache'],
            confidence: 0.70,
            advice: '⚠️ Get tested for COVID-19. Isolate from others. Monitor symptoms. Seek immediate care if breathing becomes difficult.'
        }
    };

    // Score each disease based on matching symptoms
    const predictions = [];
    for (const [disease, data] of Object.entries(diseaseDatabase)) {
        const matchingSymptoms = data.symptoms.filter(s => symptoms.includes(s) || originalMessage.includes(s));
        if (matchingSymptoms.length > 0) {
            const matchScore = (matchingSymptoms.length / data.symptoms.length) * data.confidence;
            predictions.push({
                disease: disease,
                confidence: Math.round(matchScore * 100),
                matchingSymptoms: matchingSymptoms,
                advice: data.advice
            });
        }
    }

    // Sort by confidence
    predictions.sort((a, b) => b.confidence - a.confidence);

    if (predictions.length === 0) {
        return 'I couldn\'t identify a specific condition from the symptoms mentioned. Please try:\n• Use our Symptom Checker for detailed analysis\n• Mention more specific symptoms\n• Consult a healthcare professional';
    }

    // Build response with top 3 predictions
    let response = '🩺 **Disease Prediction Based on Your Symptoms:**\n\n';

    const topPredictions = predictions.slice(0, 3);
    topPredictions.forEach((pred, index) => {
        response += `${index + 1}. **${pred.disease}** (${pred.confidence}% match)\n`;
        response += `   Matching symptoms: ${pred.matchingSymptoms.join(', ')}\n`;
        response += `   Advice: ${pred.advice}\n\n`;
    });

    response += '⚠️ **Important:** This is an AI prediction for informational purposes only. Please consult a healthcare professional for proper diagnosis and treatment.\n\n';
    response += '💡 **Next Steps:**\n';
    response += '• Use the Symptom Checker for detailed analysis\n';
    response += '• Find nearby clinics in the "Find Nearby Clinics" section\n';
    response += '• Seek immediate medical attention if symptoms are severe';

    return response;
}

// Initialize after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    try { updateUI(); } catch (e) { console.error('updateUI failed', e); }
    try { initReadAloudControl(); } catch (e) { console.error('ReadAloud init failed', e); }
    initEmergency();
});

document.addEventListener('DOMContentLoaded', () => {
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = profileDropdown.style.display === 'block';
            profileDropdown.style.display = isOpen ? 'none' : 'block';
            profileBtn.setAttribute('aria-expanded', String(!isOpen));
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            profileDropdown.style.display = 'none';
            profileBtn.setAttribute('aria-expanded', 'false');
        });
    }

    // Logout action
    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Logged out successfully');
            // Example:
            // window.location.href = "login.html";
        });
    }
});

function showHowItWorks() {
    const section = document.getElementById("howItWorks");
    if (!section) return;

    section.style.display = "block";

    section.scrollIntoView({
        behavior: "smooth"
    });
}

function hideHowItWorks() {
    const section = document.getElementById("howItWorks");
    if (!section) return;

    section.style.display = "none";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function hideAllSections() {
    const sections = [
        "onboarding",
        "symptomsSection",
        "historySection"
    ];

    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });
}

function openHistorySection() {
    hideAllSections();
    document.getElementById("historySection").style.display = "block";
    loadHistory();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function backToOnboarding() {
    hideAllSections();
    document.getElementById("onboarding").style.display = "block";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function loadHistory() {
    const list = document.getElementById("historyList");
    list.innerHTML = "";

    const history = JSON.parse(localStorage.getItem("healthHistory")) || [];

    if (history.length === 0) {
        list.innerHTML = "<p>No records available yet.</p>";
        return;
    }

    history.forEach(item => {
        const card = document.createElement("div");
        card.className = "history-card";
        card.innerHTML = `
            <h4>${item.date}</h4>
            <p><strong>Symptoms:</strong> ${item.symptoms.join(", ")}</p>
            <p><strong>Prediction:</strong> ${item.prediction}</p>
        `;
        list.appendChild(card);
    });
}

function updateStepper(step) {
    document.querySelectorAll(".step").forEach(s => {
        const n = Number(s.dataset.step);
        s.classList.remove("active", "completed");
        if (n < step) s.classList.add("completed");
        if (n === step) s.classList.add("active");
    });
}

// Persist language on change
function saveCurrentLanguage() {
    const gtCombo = document.querySelector('.goog-te-combo');
    if (gtCombo) {
        localStorage.setItem('selectedLanguage', gtCombo.value);
    }
}

// Restore language after Translate loads (call this in loadGoogleTranslate callback)
function restoreLanguage() {
    const savedLang = localStorage.getItem('selectedLanguage');
    if (savedLang && savedLang !== 'en') {
        setTimeout(() => {
            const gtCombo = document.querySelector('.goog-te-combo');
            if (gtCombo) {
                gtCombo.value = savedLang;
                gtCombo.dispatchEvent(new Event('change'));
            }
        }, 1000); // Wait for Translate to fully load
    }
}

// Update loadGoogleTranslate function to include restore
function loadGoogleTranslate() {
    new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_element');
    restoreLanguage(); // Add this line
}

// Listen for language changes
document.addEventListener('DOMContentLoaded', () => {
    const observer = new MutationObserver(() => {
        const gtCombo = document.querySelector('.goog-te-combo');
        if (gtCombo) {
            gtCombo.addEventListener('change', saveCurrentLanguage);
            observer.disconnect();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
});

let isSpeaking = false;
let utterance;

// Initialize Read Aloud Control
function initReadAloudControl() {
    const readAloudToggle = document.getElementById("readAloudToggle");
    if (readAloudToggle) {
        readAloudToggle.addEventListener("click", () => {
            const panel = document.getElementById("readAloudPanel");
            if (panel) {
                panel.style.display = panel.style.display === "block" ? "none" : "block";
            }
        });
    }
    
    const speechSpeed = document.getElementById("speechSpeed");
    if (speechSpeed) {
        speechSpeed.addEventListener("input", function () {
            const speedValue = document.getElementById("speedValue");
            if (speedValue) speedValue.innerText = this.value + "x";
        });
    }
    
    console.log("Read Aloud control initialized");
}

// Load Emergency Profile for Dashboard
function loadEmergencyProfileDashboard() {
    const profile = JSON.parse(localStorage.getItem("emergencyProfile")) || {};
    
    const dashName = document.getElementById("dashName");
    const dashAge = document.getElementById("dashAge");
    const dashBlood = document.getElementById("dashBlood");
    const dashAllergies = document.getElementById("dashAllergies");
    const dashChronic = document.getElementById("dashChronic");
    const dashMeds = document.getElementById("dashMeds");
    const dashLastUpdate = document.getElementById("dashLastUpdate");
    
    if (dashName) dashName.innerText = profile.name || "Not set";
    if (dashAge) dashAge.innerText = profile.age || "Not set";
    if (dashBlood) dashBlood.innerText = profile.blood || "Not set";
    if (dashAllergies) dashAllergies.innerText = profile.allergies || "Not set";
    if (dashChronic) dashChronic.innerText = profile.conditions || "Not set";
    if (dashMeds) dashMeds.innerText = profile.meds || "Not set";
    if (dashLastUpdate) dashLastUpdate.innerText = new Date().toLocaleString();
}

// Detect current language (Google Translate compatible)
function getCurrentLanguage() {
    // 1. Try Google Translate combo box (MOST RELIABLE)
    const gtCombo = document.querySelector(".goog-te-combo");
    if (gtCombo && gtCombo.value) {
        return gtCombo.value;
    }

    // 2. Fallback to cookie
    const match = document.cookie.match(/googtrans=\/\w+\/(\w+)/);
    if (match) return match[1];

    // 3. Default
    return "en";
}

// Get suitable voice
function getVoice(lang) {
    const voices = speechSynthesis.getVoices();

    // Exact match (hi-IN, te-IN, etc.)
    let voice = voices.find(v => v.lang === `${lang}-IN`);

    // Partial match (hi, te, mr, gu, bn)
    if (!voice) {
        voice = voices.find(v => v.lang.startsWith(lang));
    }

    // Fallback to English
    return voice || voices.find(v => v.lang.startsWith("en")) || voices[0];
}

// Speak function with text chunking for large content
function speak(text) {
    stopReading();
    
    if (!text || text.trim().length === 0) {
        alert("No text to read.");
        return;
    }

    // Limit text length to prevent browser hanging
    const maxLength = 3000;
    const textToSpeak = text.length > maxLength ? text.substring(0, maxLength) + "... (text truncated)" : text;

    const speedEl = document.getElementById("speechSpeed");
    const speed = speedEl ? parseFloat(speedEl.value) : 1;
    const lang = getCurrentLanguage();

    utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = lang;
    utterance.rate = speed;
    utterance.pitch = 1;
    utterance.voice = getVoice(lang);

    isSpeaking = true;
    speechSynthesis.speak(utterance);

    utterance.onend = () => isSpeaking = false;
    utterance.onerror = (e) => {
        console.error('Speech error:', e);
        isSpeaking = false;
    };
}

// Read whole page
function readWholePage() {
    const main = document.querySelector("main");
    if (!main) {
        alert("No content to read.");
        return;
    }
    const text = main.innerText;
    speak(text);
}

// Read selected text
function readSelectedText() {
    const selectedText = window.getSelection().toString();
    if (!selectedText) {
        alert("Please select some text first.");
        return;
    }
    speak(selectedText);
}

// Stop reading
function stopReading() {
    speechSynthesis.cancel();
    isSpeaking = false;
}

// Required for Chrome - load voices
let voicesLoaded = false;
speechSynthesis.onvoiceschanged = () => {
    voicesLoaded = true;
};

// Emergency System
let emergencyContacts = JSON.parse(localStorage.getItem('emergencyContacts') || '[]');
function detectUserLocation() {
    if (!navigator.geolocation) {
        updateStatus('❌ Geolocation not supported by this browser.');
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            updateStatus('📍 Location detected successfully.');

            saveEmergencyReport({
                location: {
                    lat: userLocation.lat,
                    lng: userLocation.lng,
                    map: `https://maps.google.com/?q=${userLocation.lat},${userLocation.lng}`
                },
                symptoms: selectedSymptoms.length ? [...selectedSymptoms] : ["Critical Emergency"],
                hospitalsFound: 0,
                contactsNotified: emergencyContacts.length
            });

            notifyNearbyHospitals();

        },
        (error) => {
            console.error('Geolocation error:', error);

            if (error.code === error.PERMISSION_DENIED) {
                updateStatus(
                    '❌ Location access denied.<br>' +
                    'Please allow location from the browser 🔒 icon and retry Emergency.'
                );
            }
            else if (error.code === error.POSITION_UNAVAILABLE) {
                updateStatus('⚠️ Location unavailable. Please check GPS or network.');
            }
            else if (error.code === error.TIMEOUT) {
                updateStatus('⏳ Location request timed out. Retrying…');
                // 🔁 retry once
                setTimeout(detectUserLocation, 1000);
            }
            else {
                updateStatus('❌ Unable to detect location.');
            }
        },
        {
            enableHighAccuracy: true,
            timeout: 20000,   // ⬅ increased timeout
            maximumAge: 0
        }
    );
}

function showRetryLocationButton() {
    const updates = document.getElementById('statusUpdates');
    if (!updates) return;

    updates.innerHTML += `
        <div style="margin-top:10px;">
            <button 
                onclick="checkLocationPermission()" 
                style="
                    padding:10px 16px;
                    border:none;
                    border-radius:20px;
                    background:#1e88e5;
                    color:white;
                    cursor:pointer;
                ">
                📍 Retry Location
            </button>
        </div>
    `;
}

function triggerEmergency() {
    emergencyMode = true;
    showEmergencyStatus();
    updateStatus('🚨 Emergency activated');
    updateStatus('📍 Requesting your current location…');
    detectUserLocation();
    buildCommonEmergencyMessage();
}

async function notifyNearbyHospitals() {
    const hospitalBox = document.getElementById("hospitalResults");
    const hospitalList = document.getElementById("hospitalList");
    if (!hospitalBox || !hospitalList) return;

    hospitalBox.style.display = "block";
    hospitalList.innerHTML = "<p>🔍 Finding nearby hospitals...</p>";

    if (!userLocation) {
        hospitalList.innerHTML = "<p>⚠️ Location is unavailable. Please allow location access and try again.</p>";
        return;
    }

    try {
        const response = await fetch(`/api/locations/nearby/?lat=${userLocation.lat}&lng=${userLocation.lng}&radius=5000`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Location service unavailable");

        const hospitals = (data.results || []).filter(p => p.type === 'hospital').map(h => ({
            ...h,
            distance: calculateGeoDistance(userLocation.lat, userLocation.lng, h.lat, h.lng)
        })).sort((a,b) => a.distance - b.distance).slice(0, 10);

        if (!hospitals.length) {
            hospitalList.innerHTML = "<p>⚠️ No mapped hospitals found within 5 km. Call 112 for emergency assistance.</p>";
            return;
        }
        showHospitalsOnMap(hospitals);
        saveNearestHospital(hospitals);
        updateStatus(`✅ Found ${hospitals.length} nearby hospitals.`);
    } catch (error) {
        console.error(error);
        hospitalList.innerHTML = `<p>⚠️ ${error.message}</p>`;
    }
}

function calculateGeoDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2-lat1) * Math.PI/180;
    const dLon = (lon2-lon1) * Math.PI/180;
    const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function notifyEmergencyContacts() {
    if (!emergencyContacts || emergencyContacts.length === 0) {
        updateStatus('⚠️ No emergency contacts configured.');
        return;
    }

    const emergencyMsg = buildCommonEmergencyMessage();

    updateStatus('📲 Emergency contacts:');

    emergencyContacts.forEach(contact => {
        const waUrl = `https://wa.me/${contact.phone}?text=${emergencyMsg}`;

        const updates = document.getElementById('statusUpdates');
        updates.innerHTML += `
            <div style="margin-top:8px; padding:6px; border-left:3px solid #25D366;">
                📞 <strong>${contact.name}</strong><br>
                <a href="${waUrl}" target="_blank">
                    Send WhatsApp Emergency Message
                </a>
            </div>
        `;
    });

    updateStatus('ℹ️ WhatsApp will open in a new tab. Please tap SEND.');
}

function showEmergencyStatus() {
    // Remove existing emergency status if any
    const existing = document.getElementById('emergencyStatus');
    if (existing) existing.remove();
    
    const statusDiv = document.createElement('div');
    statusDiv.id = 'emergencyStatus';
    statusDiv.className = 'emergency-status';
    statusDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10000;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.5);
    `;
    statusDiv.innerHTML = `
    <div style="background: linear-gradient(45deg, #ff4757, #ff3838); color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: bold;">
      <div style="font-size: 24px; margin-bottom: 10px;">🚨 EMERGENCY ACTIVATED 🚨</div>
      <div id="statusUpdates" style="font-size: 14px; margin-top: 10px; text-align: left; max-height: 300px; overflow-y: auto;"></div>
      <div id="hospitalResults" style="display:none; margin-top: 15px; text-align: left;"></div>
      <div id="hospitalList"></div>
      <button onclick="stopEmergency()" style="margin-top: 15px; padding: 12px 24px; background: white; color: #ff3838; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">❌ CANCEL EMERGENCY</button>
    </div>
  `;
    document.body.appendChild(statusDiv);
    
    // Add backdrop
    const backdrop = document.createElement('div');
    backdrop.id = 'emergencyBackdrop';
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        z-index: 9999;
    `;
    document.body.appendChild(backdrop);
}

function updateStatus(message) {
    const updates = document.getElementById('statusUpdates');
    if (updates) {
        updates.innerHTML += `<div>${message}</div>`;
    }
}

function stopEmergency() {
    document.getElementById('emergencyStatus')?.remove();
    document.getElementById('emergencyBackdrop')?.remove();
    emergencyMode = false;
}

function addEmergencyContact(name, phone) {
    name = (name || '').trim();
    phone = (phone || '').trim();

    if (!name || !phone) {
        alert('Please enter both name and phone number.');
        return;
    }

    // Simple phone cleanup
    // Clean phone number for WhatsApp (India)
    phone = phone.replace(/[^0-9]/g, '');

    // If user enters 10-digit number
    if (phone.length === 10) {
        phone = '91' + phone;
    }

    // Remove leading zero
    if (phone.startsWith('0')) {
        phone = '91' + phone.substring(1);
    }

    emergencyContacts.push({ name, phone });
    localStorage.setItem('emergencyContacts', JSON.stringify(emergencyContacts));

    renderEmergencyContacts();
    alert('Emergency contact added.');
}

function renderEmergencyContacts() {
    const listDiv = document.getElementById('contactsList');
    if (!listDiv) return;

    if (emergencyContacts.length === 0) {
        listDiv.innerHTML = '<p>No emergency contacts added yet.</p>';
        return;
    }

    listDiv.innerHTML = emergencyContacts
        .map(
            (c, idx) =>
                `<div>
           ${idx + 1}. <strong>${c.name}</strong> - ${c.phone}
         </div>`
        )
        .join('');
}

// Called directly from the button in HTML
function handleAddEmergencyContact() {
    const nameInput = document.getElementById('contactName');
    const phoneInput = document.getElementById('contactPhone');
    if (!nameInput || !phoneInput) {
        alert('Contact inputs not found on this page.');
        return;
    }
    addEmergencyContact(nameInput.value, phoneInput.value);
}

// When settings page loads, show saved contacts
document.addEventListener('DOMContentLoaded', () => {
    renderEmergencyContacts();
});

function showNearbyHospitals(hospitals) {
    const updates = document.getElementById('statusUpdates');
    if (!updates) return;

    const emergencyMsg = buildCommonEmergencyMessage();

    hospitals.slice(0, 5).forEach(h => {
        const mapLink = `https://maps.google.com/?q=${h.lat},${h.lng}`;
        const emailLink = `mailto:?subject=Emergency Alert&body=${emergencyMsg}`;
        const smsLink = `sms:?body=${emergencyMsg}`;

        updates.innerHTML += `
        <div style="margin-top:12px; padding:12px; border-left:4px solid red;">
            🏥 <strong>${h.name}</strong><br><br>

            📍 <a href="${mapLink}" target="_blank">Open in Maps</a><br>

            📞 <a href="tel:108">Call Emergency (108)</a><br>

            📧 <a href="${emailLink}">Send Emergency Email</a><br>

            📱 <a href="${smsLink}">Send Emergency SMS</a><br>

            📤 <a href="https://wa.me/?text=${emergencyMsg}" target="_blank">
                Share via WhatsApp
            </a>
        </div>
        `;
    });
}

function buildCommonEmergencyMessage() {
    const profile = JSON.parse(localStorage.getItem("emergencyProfile")) || {};
    const gpsLink = userLocation
        ? `https://maps.google.com/?q=${userLocation.lat},${userLocation.lng}`
        : "Location unavailable";

    return encodeURIComponent(
        `🚨 EMERGENCY ALERT 🚨\n\n` +
        `Name: ${profile.name || "Unknown"}\n` +
        `Age: ${profile.age || "N/A"}\n` +
        `Blood Group: ${profile.blood || "N/A"}\n` +
        `Allergies: ${profile.allergies || "None"}\n` +
        `Conditions: ${profile.conditions || "None"}\n` +
        `Medications: ${profile.meds || "None"}\n\n` +
        `📍 Location: ${gpsLink}\n\n` +
        `Immediate medical assistance required.\n` +
        `— Sent via Check MyCure`
    );
}

function initEmergency() {
    const emergencyBtn = document.getElementById('emergencyBtn');

    if (!emergencyBtn) {
        console.warn('Emergency button not found in DOM');
        return;
    }

    emergencyBtn.addEventListener('click', () => {
        triggerEmergency();
    });
}

function saveEmergencyReport(data) {
    const userKey = localStorage.getItem("userName") || "guest";
    const reports = JSON.parse(
        localStorage.getItem(`emergencyReports_${userKey}`) || "[]"
    );

    reports.unshift({
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        user: localStorage.getItem("userName") || "Guest",
        location: data.location || null,
        symptoms: data.symptoms || ["Not specified"],
        hospitalsFound: data.hospitalsFound || 0,
        contactsNotified: data.contactsNotified || 0
    });

    localStorage.setItem(`emergencyReports_${userKey}`, JSON.stringify(reports));
    
    // Also save to general emergency reports
    const allReports = JSON.parse(localStorage.getItem("emergencyReports") || "[]");
    allReports.unshift(reports[0]);
    localStorage.setItem("emergencyReports", JSON.stringify(allReports));
}

function setGoogleTranslateLang(lang) {
    const select = document.querySelector('.goog-te-combo');
    if (!select) return;

    select.value = lang;
    select.dispatchEvent(new Event('change'));

    localStorage.setItem('siteLang', lang);
}

window.addEventListener('load', () => {
    const lang = localStorage.getItem('siteLang');
    if (lang) {
        setTimeout(() => setGoogleTranslateLang(lang), 1000);
    }
});

function loadEmergencyReports() {
    const reports = JSON.parse(localStorage.getItem("emergencyReports")) || [];
    const list = document.getElementById("emergencyReportsList");
    const count = document.getElementById("emergencyCount");

    if (count) count.textContent = reports.length;

    if (!list) return;

    if (reports.length === 0) {
        list.innerHTML = "<li>No emergency reports yet.</li>";
        return;
    }

    list.innerHTML = "";

    reports.forEach(r => {
        const li = document.createElement("li");
        li.innerHTML = `
            🚨 <strong>${r.timestamp}</strong><br>
            👤 ${r.user}<br>
            🩺 ${r.symptoms.join(", ")}<br>
            🏥 Hospitals Found: ${r.hospitalsFound}<br>
            📞 Contacts Notified: ${r.contactsNotified}<br>
            ${r.location ? `<a href="${r.location.map}" target="_blank">📍 View Location</a>` : ""}
        `;
        list.appendChild(li);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadEmergencyReports();
    loadEmergencyProfileDashboard();
});


function goToSymptomChecker() {
    window.location.href = "index.html?symptom=true";
}

function showNearbyHospitalsForChatbot(hospitals) {
    const container = document.getElementById("hospitalResults");
    const list = document.getElementById("hospitalList");

    if (!container || !list) return;

    list.innerHTML = "";

    hospitals.slice(0, 8).forEach(h => {
        const mapLink = `https://maps.google.com/?q=${h.lat},${h.lng}`;

        list.innerHTML += `
            <div style="margin-bottom:10px;">
                🏥 <strong>${h.name}</strong><br>
                📍 <a href="${mapLink}" target="_blank">View on Map</a>
            </div>
        `;
    });

    container.style.display = "block";
}

function handleBotMessage(text) {
    // Hidden escalation signal
    if (text === "__AUTO_ESCALATE_HOSPITALS__") {
        appendMessage("🚑 I'm finding nearby hospitals for you now.", "bot");
        findHospitalsNormally();
        sendEmergencyNotification();
        return;
    }

    appendMessage(text, "bot");
}

const dangerKeywords = [
    "chest pain",
    "can't breathe",
    "cannot breathe",
    "fainted",
    "severe dizziness",
    "blood"
];

function checkEmergency(text) {
    const lower = text.toLowerCase();
    return dangerKeywords.some(k => lower.includes(k));
}

function detectEmotion(text) {
    if (text.includes("panic") || text.includes("help")) return "panic";
    if (text.includes("stress") || text.includes("anxious")) return "stressed";
    return null;
}

// Emergency detection is handled inside detectEmotion function

function showEmergencyUI() {
    alert("🚨 This may be serious. Please seek immediate medical help.");
    // Optional
    notifyNearbyHospitals();
}

function typeBotMessage(text) {
    const chatBox = document.getElementById("chat-messages");
    const msg = document.createElement("div");
    msg.className = "bot-message";
    chatBox.appendChild(msg);

    let i = 0;
    const interval = setInterval(() => {
        msg.innerText = text.slice(0, i++);
        chatBox.scrollTop = chatBox.scrollHeight;
        if (i > text.length) clearInterval(interval);
    }, 20);
}

document.addEventListener("DOMContentLoaded", () => {
    const hash = window.location.hash.replace("#", "");

    if (hash === "symptoms") openSymptomFromHeader();
    else if (hash === "chatbot") openChatbotFromHeader();
    else if (hash) showSection(hash);
});

function openSymptomFromHeader() {
    // reset stepper to step 1
    flowState.step = 1;
    goToStep(1);
    showSection("symptoms");

    // scroll smoothly
    document.getElementById("symptoms")
        .scrollIntoView({ behavior: "smooth" });
}

function openChatbotFromHeader() {
    showSection("chatbot");

    document.getElementById("chatbot")
        .scrollIntoView({ behavior: "smooth" });
}

function speakLastMessage() {
    const chatBox = document.getElementById("chat-messages");
    if (!chatBox || chatBox.children.length === 0) {
        alert("No messages to read");
        return;
    }

    const lastMsg = chatBox.lastElementChild.innerText;

    stopReading(); // stop previous speech

    const lang = getCurrentLanguage();
    const utterance = new SpeechSynthesisUtterance(lastMsg);
    utterance.lang = lang;
    utterance.voice = getVoice(lang);

    speechSynthesis.speak(utterance);
}

function readSelectedSymptomsFromDropdown() {
    const select = document.getElementById("symptomSelect");
    if (!select) return [];

    return Array.from(select.selectedOptions).map(opt => opt.value);
}

// Initialize symptom dropdowns after DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("categorySelect");
    const symptomSelect = document.getElementById("symptomSelect");

    if (categorySelect && symptomSelect) {
        // When category changes, populate the symptoms dropdown
        categorySelect.addEventListener("change", () => {
            const category = categorySelect.value;

            // Clear previous options
            symptomSelect.innerHTML = "";
            selectedSymptoms = [];
            const preview = document.getElementById("selectedSymptomsPreview");
            if (preview) preview.innerHTML = "";

            if (!category) {
                symptomSelect.disabled = true;
                return;
            }

            symptomSelect.disabled = false;

            // Get symptoms for this category
            const symptoms = symptomCategories[category];
            if (symptoms && symptoms.length > 0) {
                symptoms.forEach(symptom => {
                    const option = document.createElement("option");
                    option.value = symptom.toLowerCase().replace(/\s+/g, "_");
                    option.textContent = symptom;
                    symptomSelect.appendChild(option);
                });
            }
        });

        // When symptoms are selected, update the preview
        symptomSelect.addEventListener("change", () => {
            selectedSymptoms = Array.from(symptomSelect.selectedOptions)
                .map(opt => opt.textContent);

            const preview = document.getElementById("selectedSymptomsPreview");
            if (preview) {
                preview.innerHTML = selectedSymptoms.length
                    ? `Selected: ${selectedSymptoms.join(", ")}`
                    : "";
            }
        });

        console.log("Symptom dropdowns initialized successfully");
    }
});

// SOS button handler - only attach if element exists
document.addEventListener("DOMContentLoaded", () => {
    const sosBtn = document.getElementById("sosBtn");
    if (sosBtn) {
        sosBtn.addEventListener("click", () => {
            navigator.geolocation.getCurrentPosition(pos => {
                fetch("/api/sos/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        lat: pos.coords.latitude,
                        lon: pos.coords.longitude
                    })
                })
                    .then(res => res.json())
                    .then(data => {
                        window.open(`https://wa.me/?text=${encodeURIComponent(data.message)}`);
                    });
            });
        });
    }
});

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

let voiceEmergencyTriggered = false;

let recognition;

function startVoiceChatInput() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-IN";
    recognition.onresult = e => {
        document.getElementById("chat-input").value = e.results[0][0].transcript;
        sendMessage();
    };
    recognition.start();
}

function loadEmergencyProfile() {
    const profile = JSON.parse(localStorage.getItem("emergencyProfile"));
    if (!profile) return;

    dashName.innerText = profile.name || "Not set";
    dashAge.innerText = profile.age || "Not set";
    dashBlood.innerText = profile.blood || "Not set";
    dashAllergies.innerText = profile.allergies || "Not set";
    dashChronic.innerText = profile.conditions || "Not set";
    dashMeds.innerText = profile.meds || "Not set";
    dashLastUpdate.innerText = new Date().toLocaleString();
}
document.addEventListener("DOMContentLoaded", loadEmergencyProfile);

function sendQuick(text) {
    document.getElementById("chat-input").value = text;
    sendMessage();
}

function detectVoiceEmergency(text) {
    const dangerPhrases = [
        "chest pain",
        "chest hurts",
        "can't breathe",
        "cannot breathe",
        "dizzy",
        "fainted",
        "blood",
        "shortness of breath"
    ];

    return dangerPhrases.some(p => text.includes(p));

    if (emotion === "panic" && detectVoiceEmergency(text)) {
        appendMessage(
            "🚨 I hear panic and serious symptoms. Activating emergency help now.",
            "bot"
        );

        triggerEmergency();   // 🚑 hospital search starts
        return;
    }

}

function findHospitalsNormally() {
    emergencyMode = false;

    // Ensure emergency UI is hidden
    const panel = document.getElementById("emergencyPanel");
    if (panel) panel.style.display = "none";

    findNearbyHospitals();
}

function showHospitalsOnMap(hospitals) {
    const list = document.getElementById("hospitalList");
    list.innerHTML = "";

    hospitals.forEach(h => {
        const card = document.createElement("div");
        card.className = "hospital-card";

        card.innerHTML = `
      <strong>${h.name}</strong><br>
      📍 ${h.distance} km<br>
      ☎ ${h.phone || "Not available"}<br>
      <a href="tel:${h.phone}" class="call-btn">📞 Call Hospital</a>
    `;

        list.appendChild(card);
    });
}

function logHealthActivity(type) {
    const stats = JSON.parse(localStorage.getItem("healthStats")) || {
        visits: 0,
        emergencies: 0
    };

    if (type === "visit") stats.visits++;
    if (type === "emergency") stats.emergencies++;

    localStorage.setItem("healthStats", JSON.stringify(stats));
}

// Service worker registration
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("service-worker.js")
        .then(() => console.log("✅ Service Worker registered"))
        .catch(err => console.log("Service Worker registration failed:", err));
}

function sendEmergencyNotification() {
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    } else {
        navigator.serviceWorker.ready.then(reg => {
            reg.showNotification("🚨 Medical Emergency", {
                body: "Nearby hospitals are being located.",
                icon: "logo.png"
            });
        });
    }
}

// Rasa socket connection disabled - using Django backend chatbot instead
// If you want to enable Rasa, uncomment the code below and start Rasa server
/*
if (typeof io !== 'undefined') {
    try {
        const socket = null;
        socket.on("connect", () => console.log("Connected to Rasa"));
        socket.on("bot_uttered", (data) => {
            if (data.text) handleBotMessage(data.text);
        });
    } catch (e) {
        console.log("Rasa socket not available");
    }
}
*/

function updateAnalytics(type) {
    const analytics = JSON.parse(localStorage.getItem("analytics")) || {
        totalChats: 0,
        emergencies: 0,
        normalChats: 0
    };

    analytics.totalChats++;

    if (type === "emergency") analytics.emergencies++;
    else analytics.normalChats++;

    localStorage.setItem("analytics", JSON.stringify(analytics));
}

function autoCallEmergency() {
    const profile = JSON.parse(localStorage.getItem("emergencyProfile"));
    if (!profile || !profile.phone) {
        alert("⚠️ Emergency contact not set.");
        return;
    }

    const confirmCall = confirm(
        "🚨 Critical emergency detected!\nCall emergency contact now?"
    );

    if (confirmCall) {
        window.location.href = `tel:${profile.phone}`;
    }
}

function saveNearestHospital(hospitals) {
    if (!hospitals || hospitals.length === 0) return;

    hospitals.sort((a, b) => a.distance - b.distance);

    localStorage.setItem(
        "nearestHospital",
        JSON.stringify(hospitals[0])
    );
}

// saveNearestHospital is called when hospitals are found, not at load time

function autoCallNearestHospital() {
    const hospital = JSON.parse(localStorage.getItem("nearestHospital"));

    if (!hospital || !hospital.phone) {
        alert("⚠️ No hospital phone number available.");
        return;
    }

    const confirmCall = confirm(
        `🚨 Critical emergency detected!\n\nCall ${hospital.name}?`
    );

    if (confirmCall) {
        window.location.href = `tel:${hospital.phone}`;
    }
}

function saveSymptomHistory(symptoms) {
    const history = JSON.parse(localStorage.getItem("symptomHistory")) || [];

    history.push({
        symptoms,
        date: new Date().toISOString()
    });

    localStorage.setItem("symptomHistory", JSON.stringify(history));
}

// saveSymptomHistory is called when symptoms are submitted, not at load time

function predictSymptomTrend() {
    const history = JSON.parse(localStorage.getItem("symptomHistory")) || [];
    if (history.length < 3) return "Insufficient data";

    const last3 = history.slice(-3);
    const counts = {};

    last3.forEach(entry => {
        entry.symptoms.forEach(s => {
            counts[s] = (counts[s] || 0) + 1;
        });
    });

    const highFrequency = Object.values(counts).some(c => c >= 3);
    return highFrequency ? "⚠️ Worsening trend detected" : "✅ Stable trend";
}

function calculateSeverity(symptoms) {
    const weights = {
        "chest pain": 5,
        "shortness of breath": 5,
        "seizures": 5,
        "dizziness": 3,
        "fever": 2,
        "cough": 1
    };

    return symptoms.reduce(
        (sum, s) => sum + (weights[s.toLowerCase()] || 1),
        0
    );
}

function saveSeverity(score) {
    const severity = JSON.parse(localStorage.getItem("severityHistory")) || [];
    severity.push({
        score,
        date: new Date().toLocaleString()
    });
    localStorage.setItem("severityHistory", JSON.stringify(severity));
}

saveSeverity(calculateSeverity(selectedSymptoms));

function callHospitalAmbulance(hospital) {
    if (!hospital || !hospital.phone) return;
    window.location.href = `tel:${hospital.phone}`;
}

let ambulanceMap, ambulanceMarker;

function startAmbulanceTracking(userLat, userLng) {

    document.getElementById("ambulanceTracking").style.display = "block";
    document.getElementById("ambulanceStatus").innerText =
        "🚑 Ambulance is on the way...";

    ambulanceMap = L.map("ambulanceMap").setView([userLat, userLng], 14);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap"
    }).addTo(ambulanceMap);

    ambulanceMarker = L.marker([userLat + 0.01, userLng + 0.01], {
        icon: L.icon({
            iconUrl: "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
            iconSize: [40, 40]
        })
    }).addTo(ambulanceMap)
        .bindPopup("🚑 Ambulance")
        .openPopup();

    simulateAmbulanceMovement(userLat, userLng);
}

function simulateAmbulanceMovement(targetLat, targetLng) {
    let lat = targetLat + 0.01;
    let lng = targetLng + 0.01;

    const interval = setInterval(() => {
        lat -= 0.0005;
        lng -= 0.0005;

        ambulanceMarker.setLatLng([lat, lng]);
        ambulanceMap.panTo([lat, lng]);

        if (Math.abs(lat - targetLat) < 0.0005) {
            clearInterval(interval);
            document.getElementById("ambulanceStatus").innerText =
                "✅ Ambulance has arrived!";
        }
    }, 2000);
}
