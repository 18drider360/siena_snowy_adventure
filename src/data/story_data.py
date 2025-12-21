"""
Story Data
Contains all narrative dialogue and cutscene content for Siena's journey
"""

# Story scenes are structured as:
# {
#     'type': 'dialogue' or 'narration',
#     'speaker': character name (or None for narration),
#     'background_image': path to background image (optional),
#     'text_position': 'top' or 'bottom' (default: 'top'),
#     'lines': list of text lines to display
# }

# === OPENING SCENES (Before Level 1) ===

OPENING_LOST = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/OPENING.png',
    'lines': [
        "It was supposed to be a simple family road trip to Antarctica...",
        "",
        "But somewhere in the snowy mountains, I got separated from my family.",
        "",
        "Now I'm lost, alone, and I don't know the way home.",
        "",
        "I have to find them. I have to get to Antarctica!",
        "",
    ]
}

OPENING_PEDRO_APPEARS = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/OPENING_PEDRO.png',
    'lines': [
        "Hello there, little one! You look lost.",
        "",
        "My name is Pedro. I travel these lands often.",
        "",
    ]
}

OPENING_PEDRO_OFFER = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/PEDRO_OFFER.png',
    'lines': [
        "Antarctica, you say? I know these mountains well.",
        "",
        "There's a shortcut - dangerous, but much faster than the main road.",
        "",
        "The path won't be easy. You'll face wild creatures,",
        "treacherous platforms, and harsh terrain.",
        "",
        "But I believe you have what it takes, Siena.",
        "",
    ]
}

OPENING_SIENA_ACCEPTS = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/SIENA_ACCEPT.png',
    'lines': [
        "I don't have much choice. The main road is too far,",
        "and I need to find my family quickly.",
        "",
        "If Pedro says there's a shortcut, I have to try it.",
        "",
        "No matter how dangerous it is.",
        "",
    ]
}

OPENING_PEDRO_TUTORIAL = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/PEDRO_TUTORIAL.png',
    'lines': [
        "Remember these basics, Siena:",
        "",
        "Use ARROW KEYS or A/D to move left and right.",
        "Press SPACE, W, or UP to jump. You can double jump in mid-air!",
        "",
        "Watch out for enemies and hazards. Collect coins for courage.",
        "",
        "I'll be waiting at the end of each stretch to guide you.",
        "Good luck, little one!",
        "",
    ]
}

# === LEVEL 1: SNOWY CABIN FOREST ===

LEVEL_1_INTRO = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_1_INTRO.png',
    'lines': [
        "This is the Winter Forest - the first leg of your journey.",
        "",
        "Friendly creatures live here, but the wild Elkman can be dangerous.",
        "",
        "Jump carefully, avoid the hazards, and you'll make it through.",
        "",
        "I'll meet you on the other side!",
        "",
    ]
}

LEVEL_1_COMPLETE_SIENA = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_1_COMPLETE_SIENA.png',
    'lines': [
        "I... I made it through the forest.",
        "",
        "That was harder than I thought it would be.",
        "",
        "Those Elkman were scary. My legs are tired.",
        "",
        "Can I really do this whole journey?",
        "",
    ]
}

LEVEL_1_COMPLETE_PEDRO = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_1_COMPLETE_PEDRO.png',
    'lines': [
        "Siena! You did wonderfully!",
        "",
        "I watched you out there. You're braver than you know.",
        "",
        "Your family would be so proud of you right now.",
        "",
        "You know... I've walked this path for a very long time.",
        "I've seen many travelers. But you? You have something special.",
        "",
    ]
}

LEVEL_1_PEDRO_FORWARD = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_1_PEDRO_FORWARD.png',
    'lines': [
        "Come. We must keep moving north.",
        "",
        "The path ahead will test you even more.",
        "",
        "But I can see it in your eyes - you're ready.",
        "",
        "Your family is waiting. Let's not keep them.",
        "",
    ]
}

# === LEVEL 2: SNOWY CABIN FOREST ===

LEVEL_2_ARRIVAL = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_2_ARRIVAL.png',
    'lines': [
        "Cozy cabins appear through the trees, half-buried in snow.",
        "",
        "This place feels... haunted. Empty.",
        "",
        "Where are all the families who lived here?",
        "",
    ]
}

LEVEL_2_ROLL_TRAINING = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_2_ROLL_TRAINING.png',
    'lines': [
        "Before we enter, let me teach you something important.",
        "",
        "The Roll. Hold DOWN while moving left or right.",
        "",
        "Use it to slip under obstacles and through tight spaces.",
        "",
        "This technique will be crucial in the village ahead.",
        "",
    ]
}

LEVEL_2_PEDRO_INTRO = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_2_PEDRO_INTRO.png',
    'lines': [
        "The Winter Cabin Village. Humans still live here, alongside Frost Golems.",
        "",
        "The golems shoot fireballs to protect their territory.",
        "The swordsmen patrol with blades drawn.",
        "",
        "They guard these homes fiercely. They don't welcome travelers.",
        "",
        "Be careful, Siena. Stay alert and keep moving forward.",
        "",
    ]
}

LEVEL_2_COMPLETE_SIENA = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_2_COMPLETE_SIENA.png',
    'lines': [
        "I made it past the Frost Golems and the swordsmen!",
        "",
        "Those fireballs were terrifying... but I dodged them!",
        "",
        "I'm getting better at this. Stronger.",
        "",
        "Maybe... maybe I really can make it all the way to Antarctica.",
        "",
    ]
}

LEVEL_2_PEDRO_PROUD = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_2_PEDRO_PROUD.png',
    'lines': [
        "Look at you! Your confidence is growing!",
        "",
        "You're learning fast, Siena. Faster than most.",
        "",
        "Some penguins have a gift for this. A gift for perseverance.",
        "",
        "You're one of them. I knew it the moment I saw you.",
        "",
    ]
}

LEVEL_2_MOUNTAIN_PREVIEW = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_2_MOUNTAIN_PREVIEW.png',
    'lines': [
        "But Siena... the next part won't be easy.",
        "",
        "The Mountain Climb. Those peaks touch the sky.",
        "",
        "The path is steep and narrow. One wrong step...",
        "",
        "Many travelers have turned back at these mountains.",
        "",
        "This is where you'll truly be tested.",
        "",
        "But I believe in you. Are you ready?",
        "",
    ]
}

# === LEVEL 3: MOUNTAIN CLIMB ===

LEVEL_3_DOUBT = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_3_DOUBT.png',
    'lines': [
        "I stare up at the mountains. They're so... huge.",
        "",
        "How am I supposed to climb all that?",
        "",
        "Maybe I should turn back. Take the long way.",
        "",
        "Maybe this shortcut was a mistake...",
        "",
    ]
}

LEVEL_3_FAMILY_MEMORY = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_3_FAMILY_MEMORY.png',
    'lines': [
        "Wait. No.",
        "",
        "I remember what Mom told me before we left:",
        "",
        "'Siena, when things get hard, remember why you're doing it.'",
        "",
        "My family. That's why.",
        "",
        "They're waiting for me. I can't give up now.",
        "",
    ]
}

LEVEL_3_PEDRO_BELIEF = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_PEDRO_BELIEF.png',
    'lines': [
        "I can see the fear in your eyes, little one.",
        "",
        "But I also see something else. Determination.",
        "",
        "Do you know why I offered to guide you?",
        "",
        "Because I've seen that look before. In penguins who achieve great things.",
        "",
        "You have it, Siena. You're stronger than these mountains.",
        "",
    ]
}

LEVEL_3_PEDRO_WARNING = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_PEDRO_WARNING.png',
    'lines': [
        "Now we face the mountains head-on.",
        "",
        "The blizzard is fierce. Stay focused through the snow.",
        "",
        "Snowy - massive ice creatures - patrol these cliffs.",
        "And the Northerners throw spears to turn travelers back.",
        "",
        "Both the weather and the guardians will test you here.",
        "",
    ]
}

LEVEL_3_SPIN_TRAINING = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_SPIN_TRAINING.png',
    'lines': [
        "You'll need a powerful technique for these mountains.",
        "",
        "The Spin Attack. Press E to unleash it.",
        "",
        "When surrounded by enemies, use it to clear a path.",
        "",
        "It will protect you when you need it most.",
        "",
    ]
}

LEVEL_3_PEDRO_ENCOURAGEMENT = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_PEDRO_ENCOURAGEMENT.png',
    'lines': [
        "You've learned so much already, Siena.",
        "",
        "Your jumping. Your rolling. Your spin attack.",
        "",
        "Use everything I've taught you to brave the blizzard.",
        "",
        "The mountain is steep, but you're ready for it.",
        "",
        "I'll be waiting at the summit. Stay strong!",
        "",
    ]
}

LEVEL_3_SUMMIT_TRIUMPH = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_3_SUMMIT_TRIUMPH.png',
    'text_position': 'bottom',
    'lines': [
        "I'm... at the top. I'm actually at the top!",
        "",
        "I can see everything from here! The forest, the cabins...",
        "",
        "All those places I fought through. I did that. ME!",
        "",
        "My wings are tired. My feet hurt. But I made it!",
        "",
    ]
}

LEVEL_3_PEDRO_REVELATION = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_PEDRO_REVELATION.png',
    'lines': [
        "I'm proud of you, Siena. So very proud.",
        "",
        "I've guided many lost souls through these mountains.",
        "",
        "For longer than you could imagine.",
        "",
        "But you... you remind me why I keep doing this.",
        "",
        "Every penguin who makes it through... it matters.",
        "",
    ]
}

LEVEL_3_NORTHERN_LIGHTS_VIEW = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_3_NORTHERN_LIGHTS_VIEW.png',
    'text_position': 'bottom',
    'lines': [
        "And there... in the distance...",
        "",
        "The Northern Lights. Dancing across the sky in green and blue.",
        "",
        "They're beautiful. Magical.",
        "",
        "And beyond them... Antarctica.",
        "",
        "My family. I'm so close now.",
        "",
    ]
}

LEVEL_3_PEDRO_FINAL_PUSH = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_3_PEDRO_FINAL_PUSH .png',
    'lines': [
        "The Northern Lights valley. The final stretch.",
        "",
        "It's the most dangerous path of all, Siena.",
        "",
        "But beyond it... your family awaits.",
        "",
        "This is where our journey together must end soon.",
        "",
        "But first, there's one more thing I must teach you.",
        "",
    ]
}

# === LEVEL 4: NORTHERN LIGHTS VALLEY ===

LEVEL_4_LIGHTS_ARRIVAL = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_4_LIGHTS_ARRIVAL.png',
    'lines': [
        "The aurora borealis fills the sky above me.",
        "",
        "Green and blue waves dancing, shimmering, alive.",
        "",
        "The air feels different here. Magical. Ancient.",
        "",
        "This is it. The final challenge.",
        "",
    ]
}

LEVEL_4_PEDRO_WARNING = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_4_PEDRO_WARNING.png',
    'lines': [
        "Siena, listen carefully.",
        "",
        "All the enemies have gathered here over time.",
        "They've made this valley their final stronghold.",
        "",
        "No traveler shall pass - that's their oath.",
        "",
        "They've become more violent than ever before.",
        "",
        "You'll need everything - your jump, your roll, your spin.",
        "",
        "Stay focused. Stay brave.",
        "",
    ]
}

LEVEL_4_PEDRO_GOODBYE = {
    'type': 'dialogue',
    'speaker': 'Pedro',
    'background_image': 'assets/images/dialogue/LEVEL_4_PEDRO_GOODBYE.png',
    'lines': [
        "There's something I must tell you.",
        "",
        "This is where we part ways, little one.",
        "",
        "I cannot go with you to Antarctica. The lights... they're my boundary.",
        "",
        "But you don't need me anymore. You're ready.",
        "",
        "You have your jump, your roll, your spin attack.",
        "",
        "Everything you need is already inside you.",
        "",
    ]
}

LEVEL_4_SIENA_READY = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/LEVEL_4_SIENA_READY.png',
    'lines': [
        "Pedro's words echo in my mind.",
        "",
        "I have to do this last part alone.",
        "",
        "But I'm not the same penguin who got lost in those mountains.",
        "",
        "I'm stronger now. Braver. Ready.",
        "",
        "Thank you, Pedro. For everything.",
        "",
    ]
}

# === ENDING (After Level 4) ===

ENDING_ARRIVAL = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/ENDING_ARRIVAL.png',
    'lines': [
        "I emerge from the valley, exhausted but alive.",
        "",
        "The aurora borealis fades behind me.",
        "",
        "And then... I see them.",
        "",
        "In the distance, familiar shapes moving across the ice.",
        "",
        "My family!",
        "",
    ]
}

ENDING_REUNION = {
    'type': 'dialogue',
    'speaker': 'Family',
    'background_image': 'assets/images/dialogue/ENDING_REUNION.png',
    'lines': [
        "SIENA! We were so worried!",
        "",
        "We searched everywhere for you!",
        "",
        "How did you find us? How did you make it through",
        "those mountains all by yourself?",
        "",
    ]
}

ENDING_SIENA_EXPLAINS = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/ENDING_SIENA_EXPLAINS.png',
    'lines': [
        "I wasn't alone...",
        "",
        "I met someone. A kind penguin named Pedro.",
        "He showed me a shortcut through the mountains.",
        "",
        "He guided me, encouraged me, believed in me.",
        "",
        "I want to thank him!",
        "",
    ]
}

ENDING_PEDRO_THANKS = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/ENDING_PEDRO_THANKS.png',
    'lines': [
        "I turn to introduce Pedro to my family.",
        "",
        "To show them the one who made this journey possible.",
        "",
        "But when I look back...",
        "",
        "He's not there.",
        "",
        "Just footprints in the snow. Already fading.",
        "",
    ]
}

ENDING_PEDRO_GONE = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/ENDING_PEDRO_GONE.png',
    'lines': [
        "Was he real? Or something more?",
        "",
        "A guardian spirit of the mountains, perhaps,",
        "who helps lost travelers find their way home?",
        "",
        "It doesn't matter now.",
        "",
    ]
}

ENDING_FINAL = {
    'type': 'narration',
    'speaker': None,
    'background_image': 'assets/images/dialogue/ENDING_FINAL.png',
    'lines': [
        "What matters is that I made it.",
        "",
        "With courage, determination, and a little help",
        "from a mysterious friend...",
        "",
        "...any journey is possible.",
        "",
        "",
        "THE END",
        "",
    ]
}

# === Story Sequence Definitions ===

# Define which scenes play for each story beat
STORY_SEQUENCES = {
    'opening': [
        OPENING_LOST,
        OPENING_PEDRO_APPEARS,
        OPENING_PEDRO_OFFER,
        OPENING_SIENA_ACCEPTS,
        OPENING_PEDRO_TUTORIAL
    ],
    'level_1_intro': [LEVEL_1_INTRO],
    'level_1_complete': [
        LEVEL_1_COMPLETE_SIENA,
        LEVEL_1_COMPLETE_PEDRO,
        LEVEL_1_PEDRO_FORWARD
    ],
    'level_2_intro': [
        LEVEL_2_ARRIVAL,
        LEVEL_2_PEDRO_INTRO
    ],
    'level_2_complete': [
        LEVEL_2_COMPLETE_SIENA,
        LEVEL_2_PEDRO_PROUD,
        LEVEL_2_MOUNTAIN_PREVIEW
    ],
    'level_3_intro': [
        LEVEL_3_DOUBT,
        LEVEL_3_FAMILY_MEMORY,
        LEVEL_3_PEDRO_BELIEF,
        LEVEL_3_PEDRO_WARNING,
        LEVEL_3_SPIN_TRAINING,
        LEVEL_3_PEDRO_ENCOURAGEMENT
    ],
    'level_3_complete': [
        LEVEL_3_SUMMIT_TRIUMPH,
        LEVEL_3_PEDRO_REVELATION,
        LEVEL_3_NORTHERN_LIGHTS_VIEW,
        LEVEL_3_PEDRO_FINAL_PUSH
    ],
    'level_4_intro': [
        LEVEL_4_LIGHTS_ARRIVAL,
        LEVEL_4_PEDRO_WARNING,
        LEVEL_4_PEDRO_GOODBYE,
        LEVEL_4_SIENA_READY
    ],
    'ending': [
        ENDING_ARRIVAL,
        ENDING_REUNION,
        ENDING_SIENA_EXPLAINS,
        ENDING_PEDRO_THANKS,
        ENDING_PEDRO_GONE,
        ENDING_FINAL
    ]
}
