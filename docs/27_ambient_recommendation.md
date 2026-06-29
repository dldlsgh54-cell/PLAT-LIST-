# Ambient Recommendation

Gemini does not freely recommend new ambient categories.

Ambient recommendations are constrained by the selected Room Profile or Journey Profile.

## Somnera

For Somnera, Gemini can only choose from categories allowed by the selected Room Profile.

Example:

- If the selected profile is Rain Room, Gemini chooses which Rain file to use from the Rain category.
- If Gemini recommends Fireplace for Rain Room, Creator OS ignores the recommendation.

## Noctis Atlas

For Noctis Atlas, Gemini can only choose from categories allowed by the selected Journey Profile.

## Rules

- Gemini may rank candidate files inside an allowed category.
- Gemini may explain why a specific ambient file fits the profile.
- Gemini may not expand the category list.
- Creator OS rules override Gemini ambient recommendations.
- Recommendations outside the profile's allowed categories are ignored or flagged.
- Room Lock and Journey Profile recipes define the allowed ambient categories.

