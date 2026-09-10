import urllib.request
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

os.makedirs('static/avatars', exist_ok=True)

# Using avataaars with exact hair and clothing parameters to guarantee strict Male and Female appearances.
avatars = {
    'boy_1.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=B1&hair=shortHairTheCaesar&clothing=hoodie&facialHairProbability=0&backgroundColor=b6e3f4',
    'boy_2.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=B2&hair=shortHairShortWaved&clothing=collarAndSweater&facialHairProbability=0&backgroundColor=ffdfbf',
    'boy_3.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=B3&hair=shortHairShortCurly&clothing=blazerAndShirt&facialHairProbability=100&facialHair=beardLight&backgroundColor=c0aede',
    
    'girl_1.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=G1&hair=longHairStraight&clothing=shirtCrewNeck&facialHairProbability=0&backgroundColor=ffcce5',
    'girl_2.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=G2&hair=longHairBob&clothing=overall&facialHairProbability=0&backgroundColor=d1f4e0',
    'girl_3.svg': 'https://api.dicebear.com/7.x/avataaars/svg?seed=G3&hair=longHairCurvy&clothing=blazerAndShirt&facialHairProbability=0&backgroundColor=ffd5dc',
}

print("Downloading strictly gendered Avataaars SVGs...")
for filename, url in avatars.items():
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(f'static/avatars/{filename}', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Done!")
