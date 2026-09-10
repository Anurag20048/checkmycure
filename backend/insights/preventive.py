def preventive_tip(disease, weather, profile):
    if disease == "dry_eye" and weather == "polluted":
        return (
            "High pollution levels detected. "
            "Avoid rubbing your eyes and wear protective glasses."
        )

    if disease == "conjunctivitis":
        return "Avoid touching your eyes and maintain good hand hygiene."

    return None
