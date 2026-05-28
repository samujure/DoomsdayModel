BASE_STYLE = """
polished pixel art, high-end pixel-art illustration, cinematic dusk lighting,
retro-futuristic city dashboard background, crisp pixels, limited palette,
clean silhouettes, glowing windows, warm/cool contrast, subtle dithering,
game-quality pixel art, no text, no UI, no logos, no people
"""

WORLD_COMPOSITION = """
wide 16:9 cityscape, layered mountains, large setting sun, river reflections,
suspension bridge on the left, futuristic skyline in the middle,
domes and observatory tower on the right, foreground trees and purple foliage,
beautiful science-fiction city, dramatic atmosphere
"""

STATE_PROMPTS = {
    "alive": "calm but tense, city lights glowing, clean sky, hopeful twilight",
    "warming": "hotter orange sky, atmospheric haze, light smoke, stressed environment",
    "burning": "visible fires on some rooftops, smoke columns, embers, orange-red glow",
    "inferno": "major firestorm, heavy black smoke, red sky, intense burning skyline",
    "burnt": "post-catastrophe burnt city, ash-gray sky, dead trees, ruined skyline, faint smoke",
    "recovering": "rain clearing smoke, blue-green sky, new greenery, repaired lights, hopeful mood",
}

NEGATIVE_PROMPT = """
photorealistic, realistic photo, smooth vector art, blurry, muddy pixels,
overly detailed texture, illegible text, fake text, watermark, logo, people,
characters, low quality, messy UI, malformed buildings
"""

LOGO_PROMPT = """
small pixel-art Earth icon with an orbital ring, purple circular badge,
clean readable silhouette, tiny glowing atmosphere, dark navy background,
retro sci-fi dashboard logo, no text, no letters
"""

FX_PROMPTS = {
    "cloud": "transparent background, pixel-art cloud sprite, soft rounded cloud, clean edges",
    "smoke_light": "transparent background, pixel-art smoke puff sprite, soft gray purple smoke",
    "smoke_heavy": "transparent background, pixel-art heavy dark smoke puff sprite",
    "fire": "transparent background, pixel-art flame sprite, orange red yellow, looping-friendly",
    "ember": "transparent background, tiny glowing pixel ember particle",
    "ash": "transparent background, gray pixel ash particle",
    "rain": "transparent background, thin blue pixel rain streak",
    "bird": "transparent background, tiny black pixel bird silhouette, side view",
}

