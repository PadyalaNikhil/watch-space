import os

os.makedirs('static/images', exist_ok=True)

ASSETS = {}

# 1. STRANGER THINGS
ASSETS['poster-stranger-things.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="st-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#07060f"/>
      <stop offset="50%" stop-color="#14081c"/>
      <stop offset="100%" stop-color="#360007"/>
    </linearGradient>
    <radialGradient id="st-glow" cx="50%" cy="58%" r="48%">
      <stop offset="0%" stop-color="#e50914" stop-opacity="0.6"/>
      <stop offset="70%" stop-color="#e50914" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
    <filter id="glow-st" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect width="400" height="600" fill="url(#st-bg)"/>
  <circle cx="200" cy="340" r="170" fill="url(#st-glow)"/>
  <path d="M0,480 Q100,470 200,485 T400,480 L400,600 L0,600 Z" fill="#040308"/>
  <g fill="#000" opacity="0.85">
    <circle cx="140" cy="465" r="5"/><circle cx="180" cy="463" r="5"/><circle cx="220" cy="466" r="5"/><circle cx="260" cy="464" r="5"/>
  </g>
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K UHD</text>
  <path d="M200,180 Q180,260 120,320 T200,450" stroke="#e50914" stroke-width="2.5" fill="none" opacity="0.5" filter="url(#glow-st)"/>
  <path d="M200,180 Q230,280 290,340 T210,460" stroke="#e50914" stroke-width="2" fill="none" opacity="0.5" filter="url(#glow-st)"/>
  <g transform="translate(200, 360)" text-anchor="middle">
    <text y="-20" fill="#e50914" font-family="'Benguiat', Georgia, serif" font-size="33" font-weight="900" letter-spacing="2" filter="url(#glow-st)">STRANGER</text>
    <text y="20" fill="#e50914" font-family="'Benguiat', Georgia, serif" font-size="33" font-weight="900" letter-spacing="2" filter="url(#glow-st)">THINGS</text>
    <line x1="-150" y1="-48" x2="150" y2="-48" stroke="#e50914" stroke-width="3" filter="url(#glow-st)"/>
    <line x1="-150" y1="32" x2="150" y2="32" stroke="#e50914" stroke-width="2" filter="url(#glow-st)"/>
  </g>
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">98% Match  ·  2024  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Sci-Fi · Horror · Mystery · Drama</text>
  </g>
</svg>'''

ASSETS['backdrop-stranger-things.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="st-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05040a"/>
      <stop offset="40%" stop-color="#14061a"/>
      <stop offset="100%" stop-color="#2a0005"/>
    </linearGradient>
    <radialGradient id="st-bd-core" cx="65%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#e50914" stop-opacity="0.5"/>
      <stop offset="60%" stop-color="#800000" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#st-bd-bg)"/>
  <circle cx="830" cy="320" r="380" fill="url(#st-bd-core)"/>
  <!-- Rift glow branches -->
  <path d="M830,100 Q780,240 680,340 T850,560" stroke="#e50914" stroke-width="4" fill="none" opacity="0.6"/>
  <path d="M830,100 Q920,260 1020,380 T880,580" stroke="#e50914" stroke-width="3" fill="none" opacity="0.5"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#030206"/>
</svg>'''

# 2. JAILER
ASSETS['poster-jailer.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="jl-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f0b06"/>
      <stop offset="50%" stop-color="#241408"/>
      <stop offset="100%" stop-color="#4a2205"/>
    </linearGradient>
    <radialGradient id="jl-glow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#E5A00D" stop-opacity="0.5"/>
      <stop offset="65%" stop-color="#B8390E" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
    <filter id="glow-jl">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="400" height="600" fill="url(#jl-bg)"/>
  <circle cx="200" cy="270" r="160" fill="url(#jl-glow)"/>
  
  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">FILM</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K UHD</text>
  
  <!-- Tiger Muthuvel Pandian Iconic Glasses Silhouette -->
  <g transform="translate(200, 240)" stroke="#E5A00D" stroke-width="4" fill="none" filter="url(#glow-jl)">
    <!-- Sunglasses frames -->
    <rect x="-85" y="-18" width="70" height="36" rx="6" fill="#110d08" stroke="#E5A00D" stroke-width="3.5"/>
    <rect x="15" y="-18" width="70" height="36" rx="6" fill="#110d08" stroke="#E5A00D" stroke-width="3.5"/>
    <line x1="-15" y1="-2" x2="15" y2="-2" stroke="#E5A00D" stroke-width="4"/>
    <!-- Intense glare highlight -->
    <line x1="-70" y1="-8" x2="-40" y2="12" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
    <line x1="30" y1="-8" x2="60" y2="12" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
  </g>

  <!-- Title: JAILER -->
  <g transform="translate(200, 370)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Impact', Arial Black, sans-serif" font-size="56" letter-spacing="6">JAILER</text>
    <text y="28" fill="#E5A00D" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="800" letter-spacing="8">SUPERSTAR RAJINIKANTH</text>
    <line x1="-130" y1="42" x2="130" y2="42" stroke="#E5A00D" stroke-width="1.5" opacity="0.6"/>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">98% Match  ·  2023  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Action · Crime · Thriller · Nelson Film</text>
  </g>
</svg>'''

ASSETS['backdrop-jailer.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="jl-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0704"/>
      <stop offset="45%" stop-color="#1f1006"/>
      <stop offset="100%" stop-color="#3d1b03"/>
    </linearGradient>
    <radialGradient id="jl-bd-core" cx="70%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#E5A00D" stop-opacity="0.45"/>
      <stop offset="60%" stop-color="#B8390E" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#jl-bd-bg)"/>
  <circle cx="880" cy="280" r="400" fill="url(#jl-bd-core)"/>
  <path d="M0,590 Q450,560 900,580 T1280,570 L1280,720 L0,720 Z" fill="#060402"/>
</svg>'''

# 3. SQUID GAME
ASSETS['poster-squid-game.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="sg-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#041617"/>
      <stop offset="50%" stop-color="#07292a"/>
      <stop offset="100%" stop-color="#2a0518"/>
    </linearGradient>
    <radialGradient id="sg-glow" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#FF1053" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#FF1053" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
    <filter id="glow-sg">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="400" height="600" fill="url(#sg-bg)"/>
  <circle cx="200" cy="280" r="160" fill="url(#sg-glow)"/>

  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K HDR</text>

  <!-- Iconic Circle, Triangle, Square symbols -->
  <g transform="translate(200, 240)" stroke="#FF1053" stroke-width="5" fill="none" filter="url(#glow-sg)">
    <circle cx="-80" cy="0" r="28"/>
    <polygon points="0,-32 -28,26 28,26"/>
    <rect x="52" y="-28" width="56" height="56" rx="4"/>
  </g>

  <!-- Title: SQUID GAME -->
  <g transform="translate(200, 365)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Impact', Arial Black, sans-serif" font-size="44" letter-spacing="4">SQUID GAME</text>
    <text y="26" fill="#03DAC6" font-family="'Helvetica Neue', Arial, sans-serif" font-size="12" font-weight="800" letter-spacing="6">SEASON 2</text>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">99% Match  ·  2025  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Thriller · Suspense · Drama · Korean</text>
  </g>
</svg>'''

ASSETS['backdrop-squid-game.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="sg-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#021011"/>
      <stop offset="50%" stop-color="#042021"/>
      <stop offset="100%" stop-color="#240314"/>
    </linearGradient>
    <radialGradient id="sg-bd-core" cx="70%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#FF1053" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#03DAC6" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#sg-bd-bg)"/>
  <circle cx="850" cy="290" r="390" fill="url(#sg-bd-core)"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#020909"/>
</svg>'''

# 4. WEDNESDAY
ASSETS['poster-wednesday.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="wd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#08080c"/>
      <stop offset="50%" stop-color="#141022"/>
      <stop offset="100%" stop-color="#21183c"/>
    </linearGradient>
    <radialGradient id="wd-glow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#8B5CF6" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="400" height="600" fill="url(#wd-bg)"/>
  <circle cx="200" cy="270" r="160" fill="url(#wd-glow)"/>

  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K UHD</text>

  <!-- Gothic silhouette & Nevermore crest -->
  <g transform="translate(200, 240)" fill="none" stroke="#C4B5FD" stroke-width="2.5">
    <path d="M-40,-30 L0,-60 L40,-30 L30,40 L0,55 L-30,40 Z"/>
    <circle cx="0" cy="-5" r="18" stroke="#8B5CF6" stroke-width="2"/>
    <line x1="0" y1="-23" x2="0" y2="13" stroke="#8B5CF6" stroke-width="2"/>
    <line x1="-18" y1="-5" x2="18" y2="-5" stroke="#8B5CF6" stroke-width="2"/>
  </g>

  <!-- Title: WEDNESDAY -->
  <g transform="translate(200, 365)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Georgia', serif" font-size="38" font-weight="700" letter-spacing="6">WEDNESDAY</text>
    <text y="26" fill="#A78BFA" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="700" letter-spacing="4">SEASON 2</text>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">96% Match  ·  2025  ·  TV-14</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Fantasy · Comedy · Mystery · Teen</text>
  </g>
</svg>'''

ASSETS['backdrop-wednesday.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="wd-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050508"/>
      <stop offset="50%" stop-color="#110d1c"/>
      <stop offset="100%" stop-color="#1c132f"/>
    </linearGradient>
    <radialGradient id="wd-bd-core" cx="70%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#wd-bd-bg)"/>
  <circle cx="850" cy="280" r="390" fill="url(#wd-bd-core)"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#030305"/>
</svg>'''

# 5. MONEY HEIST
ASSETS['poster-money-heist.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="mh-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#120404"/>
      <stop offset="50%" stop-color="#2b0808"/>
      <stop offset="100%" stop-color="#590e0e"/>
    </linearGradient>
    <radialGradient id="mh-glow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#E50914" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#E50914" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="400" height="600" fill="url(#mh-bg)"/>
  <circle cx="200" cy="270" r="160" fill="url(#mh-glow)"/>

  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K UHD</text>

  <!-- Dalí Mask Stylized Emblem -->
  <g transform="translate(200, 240)" fill="none" stroke="#FFFFFF" stroke-width="3">
    <ellipse cx="0" cy="0" rx="42" ry="58"/>
    <!-- Eyes -->
    <ellipse cx="-16" cy="-8" rx="8" ry="6" fill="#FFF"/>
    <ellipse cx="16" cy="-8" rx="8" ry="6" fill="#FFF"/>
    <!-- Iconic Dali Moustache -->
    <path d="M-30,18 Q-10,12 0,16 Q10,12 30,18 Q40,6 42,-4" stroke="#FFF" stroke-width="3.5"/>
    <path d="M30,18 Q10,12 0,16 Q-10,12 -30,18 Q-40,6 -42,-4" stroke="#FFF" stroke-width="3.5"/>
  </g>

  <!-- Title: MONEY HEIST -->
  <g transform="translate(200, 365)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Impact', Arial Black, sans-serif" font-size="44" letter-spacing="4">MONEY HEIST</text>
    <text y="26" fill="#E50914" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="800" letter-spacing="4">LA CASA DE PAPEL</text>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">97% Match  ·  2021  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Crime · Thriller · Action · Spanish</text>
  </g>
</svg>'''

ASSETS['backdrop-money-heist.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="mh-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0202"/>
      <stop offset="50%" stop-color="#240505"/>
      <stop offset="100%" stop-color="#420808"/>
    </linearGradient>
    <radialGradient id="mh-bd-core" cx="70%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#E50914" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#mh-bd-bg)"/>
  <circle cx="850" cy="280" r="390" fill="url(#mh-bd-core)"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#050101"/>
</svg>'''

# 6. THE QUEEN'S GAMBIT
ASSETS['poster-queens-gambit.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="qg-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a1210"/>
      <stop offset="50%" stop-color="#142621"/>
      <stop offset="100%" stop-color="#213d35"/>
    </linearGradient>
    <radialGradient id="qg-glow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#E5A00D" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#E5A00D" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="400" height="600" fill="url(#qg-bg)"/>
  <circle cx="200" cy="270" r="160" fill="url(#qg-glow)"/>

  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K HDR</text>

  <!-- Chess Queen Silhouette -->
  <g transform="translate(200, 240)" fill="#E5A00D" opacity="0.9">
    <circle cx="0" cy="-45" r="7"/>
    <circle cx="-28" cy="-35" r="5"/>
    <circle cx="28" cy="-35" r="5"/>
    <path d="M-30,-28 L-15,10 L15,10 L30,-28 L15,-15 L0,-38 L-15,-15 Z"/>
    <rect x="-24" y="14" width="48" height="8" rx="2"/>
    <rect x="-32" y="26" width="64" height="12" rx="3"/>
  </g>

  <!-- Title: THE QUEEN'S GAMBIT -->
  <g transform="translate(200, 365)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Georgia', serif" font-size="28" font-weight="700" letter-spacing="3">THE QUEEN'S GAMBIT</text>
    <text y="24" fill="#E5A00D" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="700" letter-spacing="4">LIMITED SERIES</text>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">95% Match  ·  2020  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Drama · Cerebral · Period Piece</text>
  </g>
</svg>'''

ASSETS['backdrop-queens-gambit.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="qg-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060c0a"/>
      <stop offset="50%" stop-color="#0f1f1a"/>
      <stop offset="100%" stop-color="#182e28"/>
    </linearGradient>
    <radialGradient id="qg-bd-core" cx="70%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#E5A00D" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#qg-bd-bg)"/>
  <circle cx="850" cy="280" r="390" fill="url(#qg-bd-core)"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#040706"/>
</svg>'''

# 7. DARK
ASSETS['poster-dark.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <defs>
    <linearGradient id="dk-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090c0f"/>
      <stop offset="50%" stop-color="#121a20"/>
      <stop offset="100%" stop-color="#1e2c36"/>
    </linearGradient>
    <radialGradient id="dk-glow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#F59E0B" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="400" height="600" fill="url(#dk-bg)"/>
  <circle cx="200" cy="270" r="160" fill="url(#dk-glow)"/>

  <!-- Netflix Red N Badge -->
  <g transform="translate(24, 28)">
    <path d="M0,0 L7,0 L18,32 L18,0 L24,0 L24,36 L17,36 L6,4 L6,36 L0,36 Z" fill="#E50914"/>
    <text x="32" y="22" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="800" letter-spacing="3">SERIES</text>
  </g>
  <rect x="310" y="28" width="66" height="20" rx="3" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
  <text x="343" y="42" fill="#FFF" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">4K UHD</text>

  <!-- Triquetra Time Loop Symbol -->
  <g transform="translate(200, 240)" fill="none" stroke="#F59E0B" stroke-width="3">
    <circle cx="0" cy="0" r="40"/>
    <path d="M0,-40 A40,40 0 0,0 -34.6,20 A40,40 0 0,0 34.6,20 A40,40 0 0,0 0,-40 Z"/>
  </g>

  <!-- Title: DARK -->
  <g transform="translate(200, 365)" text-anchor="middle">
    <text y="0" fill="#FFFFFF" font-family="'Impact', Arial Black, sans-serif" font-size="52" letter-spacing="8">DARK</text>
    <text y="26" fill="#F59E0B" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="800" letter-spacing="6">THE FINAL CYCLE</text>
  </g>

  <!-- Bottom info -->
  <g transform="translate(200, 545)" text-anchor="middle" font-family="'Helvetica Neue', Arial, sans-serif">
    <text y="0" fill="#46D369" font-size="13" font-weight="700">96% Match  ·  2020  ·  TV-MA</text>
    <text y="22" fill="#A3A3B2" font-size="11" font-weight="500">Sci-Fi · Mystery · Time Travel · German</text>
  </g>
</svg>'''

ASSETS['backdrop-dark.svg'] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <linearGradient id="dk-bd-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050709"/>
      <stop offset="50%" stop-color="#0d1419"/>
      <stop offset="100%" stop-color="#16222a"/>
    </linearGradient>
    <radialGradient id="dk-bd-core" cx="70%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#dk-bd-bg)"/>
  <circle cx="850" cy="280" r="390" fill="url(#dk-bd-core)"/>
  <path d="M0,580 Q400,550 800,570 T1280,560 L1280,720 L0,720 Z" fill="#030406"/>
</svg>'''

for name, svg in ASSETS.items():
    path = os.path.join('static', 'images', name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated {path}")

print("All Netflix assets successfully generated!")
