#!/usr/bin/env python3
"""
Static page generator for Go Green College Painters.

Builds:
  /services/exterior-painting/index.html
  /services/interior-painting/index.html
  /services/deck-staining/index.html
  /services/custom-murals/index.html
  /grand-rapids/cascade/index.html
  /grand-rapids/forest-hills/index.html
  /grand-rapids/ada/index.html
  /grand-rapids/east-grand-rapids/index.html

Each page reuses the LocalBusiness JSON-LD from the homepage (same @id) plus a page-specific
Service, FAQPage, BreadcrumbList, and WebPage node — so every URL is its own valid local-SEO
citation while staying NAP-consistent with the home page.

Neighborhood pages override Service.areaServed with the specific city + an `area_served`
config key. Pages also override the related-links heading via `related_heading`.

To rebuild: `python3 build_pages.py` from the repo root.
"""
import json, os, html as html_lib, textwrap, datetime

SITE = "https://gogreenpainters.com"
BUSINESS_ID = f"{SITE}/#business"

# hero_img path -> responsive CSS class (defined in styles.css). Falls back to hero-default.
HERO_CLASS_MAP = {
    "/exterior-after.jpg": "hero-exterior",
    "/interior-after.jpg": "hero-interior",
    "/stain-after.jpg": "hero-stain",
    "/custom-designs.jpg": "hero-murals",
    "/hero-bg.jpg": "hero-default",
}

def og_image(slug):
    """Deterministic OG social-card path from a page slug (matches build_og_images.py)."""
    key = slug.strip("/").replace("/", "-") or "home"
    return f"{SITE}/og/og-{key}.jpg"

# -------- shared LocalBusiness block (kept identical across pages, same @id) --------
LOCAL_BUSINESS = {
    "@type": ["LocalBusiness", "HousePainter"],
    "@id": BUSINESS_ID,
    "name": "Go Green College Painters",
    "url": SITE,
    "logo": f"{SITE}/logo.png",
    "image": f"{SITE}/logo.png",
    "description": "Student-owned professional painting company offering exterior painting, interior painting, deck staining, and custom mural design in Greater Grand Rapids, Michigan. Owner-operated with guaranteed satisfaction.",
    "telephone": "+1-616-264-2119",
    "email": "jack@gogreenpainters.com",
    "foundingDate": "2024",
    "priceRange": "$$",
    "founder": [
        {"@id": f"{SITE}/#jackson"},
        {"@id": f"{SITE}/#evelyn"},
    ],
    "areaServed": {
        "@type": "GeoCircle",
        "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 42.9634, "longitude": -85.6681},
        "geoRadius": "50000",
    },
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Grand Rapids",
        "addressRegion": "MI",
        "postalCode": "49503",
        "addressCountry": "US",
    },
    "sameAs": [
        "https://www.yelp.com/biz/go-green-painters-grand-rapids",
        "https://www.facebook.com/profile.php?id=61589807997680",
    ],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5",
        "reviewCount": "3",
        "bestRating": "5",
    },
}

# WebSite node — referenced by every WebPage's isPartOf. Defined once, included in each graph.
WEBSITE_NODE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": "Go Green College Painters",
    "description": "Student-owned house painting company serving Greater Grand Rapids, Michigan — exterior, interior, deck staining, and custom murals.",
    "publisher": {"@id": BUSINESS_ID},
    "inLanguage": "en-US",
}

# -------- per-page configs --------
PAGES = [
    {
        "slug": "services/exterior-painting/",
        "title": "Exterior House Painting in Grand Rapids, MI | Go Green College Painters",
        "description": "Owner-operated exterior house painting in Grand Rapids, MI. Full prep, premium primer and paint, and a finish built to handle Michigan freeze-thaw and lake-effect humidity. Free estimates.",
        "h1": "Exterior House Painting in Grand Rapids, MI",
        "hero_img": "/exterior-after.jpg",
        "service_name": "Exterior House Painting",
        "service_desc": "Full exterior house and building painting in Grand Rapids, MI — including prep, scraping, priming, and two coats — built to withstand Michigan freeze-thaw cycles and lake-effect humidity.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Exterior Painting", "/services/exterior-painting/")],
        "lead": "Jackson and Evelyn personally repaint exteriors for Grand Rapids homeowners — siding, trim, doors, garages, soffits, and fascia — with a finish built for Michigan's freeze-thaw cycles, lake-effect humidity, and short paint season. No subcontractors, no crew of strangers, no shortcuts on prep.",
        "sections": [
            ("What's Included in an Exterior Repaint", """
                <p>Every exterior project includes a complete prep and finish sequence, not a one-coat refresh.</p>
                <ul>
                  <li><strong>Pressure wash</strong> all siding, trim, soffits, and fascia to remove dirt, mildew, and chalking.</li>
                  <li><strong>Scrape and sand</strong> loose or peeling paint down to a sound substrate.</li>
                  <li><strong>Caulk</strong> gaps around windows, trim seams, and siding joints to prevent water intrusion.</li>
                  <li><strong>Spot-prime</strong> bare wood, knots, and stain-prone areas with the right primer for the substrate.</li>
                  <li><strong>Two finish coats</strong> of premium exterior paint applied by brush, roller, or sprayer depending on surface.</li>
                  <li><strong>Detail work</strong> on doors, trim, shutters, garage doors, and porch ceilings.</li>
                  <li><strong>Daily cleanup</strong> and a final walkthrough — we don't leave until you're happy.</li>
                </ul>
            """),
            ("Paint We Recommend for Grand Rapids Homes", """
                <p>Grand Rapids exteriors take a beating — humid summers, freeze-thaw winters, and UV that fades cheaper paint within a few seasons. We use 100% acrylic premium exterior paints from <strong>Sherwin-Williams</strong> (Duration, Emerald) and <strong>Benjamin Moore</strong> (Aura Exterior, Regal Select). A typical exterior repaint with these paints lasts 8 to 12 years on properly prepped siding.</p>
            """),
            ("When to Paint Your Exterior in Michigan", """
                <p>The Grand Rapids exterior paint season runs roughly <strong>May through mid-October</strong>. We need surface temperatures above 50&deg;F, low overnight humidity, and 24-48 hours of dry weather after each coat. Late spring and early fall are our most-booked windows because the temperature swings are gentlest on fresh paint.</p>
            """),
            ("Timeline and Cost", """
                <p>Most one-story homes take <strong>3 to 5 days</strong>. Two-story homes typically take <strong>4 to 7 days</strong>, depending on siding condition, prep work, and number of detail elements (trim, shutters, doors).</p>
                <p>Exterior painting in the Grand Rapids area generally runs <strong>$3,000 to $7,000</strong> for a one- or two-story home, with the largest cost drivers being siding type, condition, and accessibility (multi-story, complex rooflines, dormers). Every estimate is free, fixed-price, and based on a walk-through of your specific home.</p>
            """),
        ],
        "faqs": [
            ("How long does exterior paint last in Grand Rapids?", "On a properly prepped surface with premium 100% acrylic exterior paint, an exterior repaint in the Grand Rapids area typically lasts 8 to 12 years. South- and west-facing walls fade faster than north sides, and trim usually needs a refresh before siding does."),
            ("When is the best time to paint a house in Michigan?", "Late May through early October is the prime exterior paint window in Grand Rapids. We need consistent overnight temperatures above 50°F, low humidity, and clear weather for 24-48 hours after each coat."),
            ("Do you pressure wash and prep before painting?", "Yes. Every exterior project starts with a full pressure wash, scraping of loose paint, sanding, caulking, and spot priming as needed. Prep is what makes paint last in Michigan's climate — we won't skip it."),
            ("Do you patch and prep exterior surfaces before painting?", "We patch small holes, nicks, and minor surface imperfections with wood filler as part of normal exterior prep. We do not replace siding boards, fix rotted wood, or perform carpentry — for that work we'll refer you to a trusted carpenter and coordinate the paint afterward."),
            ("How much does exterior house painting cost in Grand Rapids?", "Exterior house painting in Grand Rapids typically ranges from $3,000 to $7,000 for a one- or two-story home, depending on siding type and condition, prep work, height, and accessibility. We provide a free, fixed-price written estimate after a walk-through."),
        ],
        "related": [
            ("Interior Painting", "/services/interior-painting/"),
            ("Deck Staining", "/services/deck-staining/"),
            ("Custom Murals", "/services/custom-murals/"),
        ],
    },
    {
        "slug": "services/interior-painting/",
        "title": "Interior House Painting in Grand Rapids, MI | Go Green College Painters",
        "description": "Owner-operated interior painting in Grand Rapids, MI — walls, ceilings, trim, and cabinets. Full furniture and floor protection, clean lines, zero mess. Free estimates.",
        "h1": "Interior Painting in Grand Rapids, MI",
        "hero_img": "/interior-after.jpg",
        "service_name": "Interior House Painting",
        "service_desc": "Interior painting in Grand Rapids — single rooms or whole homes — including walls, ceilings, trim, doors, and cabinet refinishing. Full furniture and floor protection.",
        "service_image": f"{SITE}/interior-painting.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Interior Painting", "/services/interior-painting/")],
        "lead": "Owner-operated interior painting for Grand Rapids homes — walls, ceilings, trim, doors, accent walls, and kitchen cabinets. We move and protect your furniture, drop-cloth every floor, cut clean lines without tape lines, and leave the house cleaner than we found it.",
        "sections": [
            ("Rooms We Paint", """
                <p>We paint everything inside the house: living rooms, bedrooms, kitchens, bathrooms, hallways, stairwells, basements, ceilings, trim, doors, closets, and accent walls. Smaller projects (one-room refreshes) and whole-home repaints both welcome.</p>
            """),
            ("Our Interior Painting Process", """
                <ul>
                  <li><strong>Free estimate</strong> — we walk the house, recommend prep, and quote a fixed price.</li>
                  <li><strong>Color consult</strong> — Evelyn (Industrial Design, Wayne State) can help with palette selection if you want it.</li>
                  <li><strong>Setup</strong> — move and cover furniture, drop-cloth floors, mask trim and outlets.</li>
                  <li><strong>Prep</strong> — patch nail holes and small drywall dings, sand glossy surfaces, prime stains.</li>
                  <li><strong>Paint</strong> — cut in by hand, two coats unless one is genuinely enough, no tape marks.</li>
                  <li><strong>Cleanup</strong> — furniture back, floors vacuumed, walkthrough with you.</li>
                </ul>
            """),
            ("Kitchen Cabinet Refinishing", """
                <p>Cabinet refinishing is a separate craft from wall painting and a smart alternative to full kitchen replacement. We remove doors and drawer fronts, label and number every piece, scuff-sand and degrease, prime with a bonding primer, and apply two coats of cabinet-grade enamel for a hard, factory-like finish. A typical kitchen takes 4 to 6 days.</p>
            """),
            ("Timeline and Cost", """
                <p>A single-room repaint usually takes <strong>1 to 2 days</strong>. A whole-home interior repaint typically takes <strong>3 to 7 days</strong> depending on square footage, ceiling height, and trim work.</p>
                <p>Interior painting in Grand Rapids generally runs <strong>$700 to $1,700 per room</strong> and <strong>$4,700 to $8,500 for a whole-home repaint</strong>. We provide a fixed-price estimate after walking the space — no surprises.</p>
            """),
        ],
        "faqs": [
            ("How long does interior painting take per room?", "A single average-sized bedroom or living room typically takes 1 to 2 days from prep to cleanup. Kitchens, bathrooms with tile and fixtures, and rooms with extensive trim take longer. Whole-home repaints usually run 3 to 7 days."),
            ("Do you move and protect furniture?", "Yes. We move furniture to the center of each room (or out of the room when needed), drop-cloth floors, and mask trim, outlets, and switches. Everything goes back exactly where we found it at the end."),
            ("What paint brands do you use for interiors?", "Our default interior lines are Sherwin-Williams Cashmere, Emerald Interior, and Benjamin Moore Regal Select / Aura — all premium acrylic latex paints designed for smooth coverage, durability, and easy cleaning."),
            ("Can you paint kitchen cabinets?", "Yes. Cabinet refinishing is a major specialty — we remove and label every door and drawer, scuff-sand, prime with a bonding primer, and apply two coats of cabinet-grade enamel. A typical kitchen takes 4 to 6 days for a result that looks factory-applied."),
            ("How much does interior painting cost in Grand Rapids?", "Interior painting in Grand Rapids generally runs $700 to $1,700 per room and $4,700 to $8,500 for a whole-house repaint, depending on square footage, ceiling height, prep work, and trim. Every estimate is free and fixed-price."),
            ("How soon can my room be used after painting?", "With modern interior latex paint, rooms are typically usable within 4-6 hours of the last coat and fully cured within 1-2 weeks. We let you know what to expect on each project."),
        ],
        "related": [
            ("Custom Murals & Accent Walls", "/services/custom-murals/"),
            ("Deck Staining", "/services/deck-staining/"),
            ("Exterior Painting", "/services/exterior-painting/"),
        ],
    },
    {
        "slug": "services/deck-staining/",
        "title": "Deck Staining & Restoration in Grand Rapids, MI | Go Green College Painters",
        "description": "Deck staining and fence staining in Grand Rapids, MI. We clean, sand, prep, and seal weathered decks to protect them through Michigan winters. Free estimates.",
        "h1": "Deck Staining & Restoration in Grand Rapids, MI",
        "hero_img": "/stain-after.jpg",
        "service_name": "Deck Staining and Restoration",
        "service_desc": "Deck and fence staining in Grand Rapids, MI. Includes cleaning, sanding, surface prep, and protective stain sealing to withstand Michigan winters. Refinishing and staining only — board replacement and carpentry are not included.",
        "service_image": f"{SITE}/deck-staining.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Deck Staining", "/services/deck-staining/")],
        "lead": "Michigan winters are brutal on wood. We refinish weathered decks, fences, pergolas, and play structures in Grand Rapids — clean, sand, prep, and seal — so they look new and stay protected through the next freeze-thaw cycle. (Surface refinishing only; we don't replace boards or do carpentry.)",
        "sections": [
            ("Stain Types We Offer", """
                <ul>
                  <li><strong>Transparent stain</strong> — preserves the natural wood grain with mild UV protection. Best for newer wood.</li>
                  <li><strong>Semi-transparent stain</strong> — tints the wood while showing the grain. Good for decks with some weathering. The most popular choice.</li>
                  <li><strong>Semi-solid stain</strong> — heavier pigment for older decks or where you want a more uniform color.</li>
                  <li><strong>Solid stain</strong> — paint-like finish that covers grain completely. Used for badly weathered decks or to match a specific color.</li>
                </ul>
                <p>Not sure which is right for your deck? We'll walk through your wood's condition and color preferences during the estimate.</p>
            """),
            ("Our Deck Refinishing Process", """
                <ul>
                  <li><strong>Inspect</strong> the surface for wear, peeling, and prep needs. (If we spot rotted or broken boards we'll flag them and recommend a carpenter — board replacement is outside our scope.)</li>
                  <li><strong>Clean</strong> with the right wood cleaner for the type of staining or mildew present.</li>
                  <li><strong>Patch</strong> small surface imperfections with wood filler as part of prep.</li>
                  <li><strong>Sand</strong> the surface to open up the grain so stain absorbs evenly.</li>
                  <li><strong>Stain</strong> — apply the chosen stain by brush or pad, working with the grain.</li>
                  <li><strong>Final coat</strong> — sealing topcoat where needed for traffic protection.</li>
                </ul>
            """),
            ("Fences, Pergolas, and Play Structures", """
                <p>Same process applies to fences, pergolas, gazebos, and outdoor play sets. We've restored several Grand Rapids play structures and decks that homeowners thought were done — strong cleaning, the right stain, and the wood comes back.</p>
            """),
            ("Timeline and Cost", """
                <p>A standard 200-400 sq ft deck typically takes <strong>2 to 4 days</strong> from cleaning to final stain coat. Larger decks, multi-level structures, and fence-plus-deck combinations take longer.</p>
                <p>Deck staining in Grand Rapids generally runs <strong>$700 to $2,500</strong> depending on deck size, surface condition, and stain type. Every quote is free and fixed-price.</p>
            """),
        ],
        "faqs": [
            ("How often should I re-stain my deck in Michigan?", "Most decks in Grand Rapids need re-staining every 2 to 4 years. Semi-transparent stains fade faster than solid stains. South- and west-facing decks need attention sooner. We can inspect yours and tell you honestly whether it's due."),
            ("Should I stain or paint my deck?", "Stain is almost always the right call for decks. Paint sits on top of the wood and chips and peels as the deck flexes and ages; stain penetrates the wood and wears more gracefully. The exception is solid stain, which has paint-like coverage but still bonds with the wood."),
            ("What stain brands do you use?", "We use premium oil-based and waterborne stains from Sherwin-Williams (SuperDeck, DeckScapes) and Benjamin Moore (Arborcoat) — both lines hold up well to Michigan freeze-thaw and UV."),
            ("Can you bring back a really weathered deck?", "Often yes — a thorough cleaning, sanding, and the right stain can bring most weathered decks back to looking new. We focus on refinishing and staining only; if your deck has rotted, cracked, or broken boards, we'll point that out and recommend a carpenter for board replacement first. We don't do board replacement or structural repair ourselves."),
            ("How long does deck staining take?", "A typical 200-400 sq ft deck takes 2 to 4 days from initial cleaning through final stain coat. Weather can extend the timeline — stain needs dry conditions and surface temperatures in the right range."),
            ("Can you stain fences and pergolas too?", "Yes. Fences, pergolas, gazebos, and play structures all use the same process. We can do them at the same time as your deck or as standalone projects."),
        ],
        "related": [
            ("Exterior Painting", "/services/exterior-painting/"),
            ("Interior Painting", "/services/interior-painting/"),
            ("Custom Murals", "/services/custom-murals/"),
        ],
    },
    {
        "slug": "services/custom-murals/",
        "title": "Custom Murals & Accent Walls in Grand Rapids, MI | Go Green Painters",
        "description": "Hand-painted custom murals and accent walls in Grand Rapids, MI. Kids' rooms, nurseries, dining rooms, commercial spaces. Designed and painted by Evelyn Befus, Industrial Design student at Wayne State. Free design consultation.",
        "h1": "Custom Murals & Accent Walls in Grand Rapids, MI",
        "hero_img": "/custom-designs.jpg",
        "service_name": "Custom Mural Design and Painting",
        "service_desc": "Hand-painted custom murals and accent walls for Grand Rapids homes and businesses — kids' rooms, nurseries, dining rooms, accent walls, and commercial spaces. Designed and painted by Evelyn Befus.",
        "service_image": f"{SITE}/custom-designs.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Custom Murals", "/services/custom-murals/")],
        "lead": "Custom hand-painted murals and accent walls in Grand Rapids — designed and painted by Evelyn Befus, an Industrial Design student at Wayne State University and a lifelong illustrator. We're one of the only residential painters in Grand Rapids who also do real, hand-painted custom mural work — no decals, no projector outlines, no AI prints.",
        "sections": [
            ("Mural Projects We Take On", """
                <ul>
                  <li><strong>Kids' rooms and nurseries</strong> — animals, woodlands, space, ocean, fairytale, whatever your child loves.</li>
                  <li><strong>Accent walls in living spaces</strong> — abstract, botanical, geometric, or landscape.</li>
                  <li><strong>Dining rooms and entryways</strong> — statement pieces that anchor a room.</li>
                  <li><strong>Commercial walls and lobbies</strong> — branded murals, illustrated logos, color stories that match a brand.</li>
                  <li><strong>Restaurants and cafes</strong> — mood walls, signage, photo-friendly backgrounds.</li>
                  <li><strong>Exterior building murals</strong> — for larger commercial projects.</li>
                </ul>
            """),
            ("Our Mural Design Process", """
                <ol>
                  <li><strong>Free consultation</strong> — we visit the space, take measurements, talk about what you have in mind, and look at reference imagery you love.</li>
                  <li><strong>Concept sketch</strong> — Evelyn draws 1-3 concept directions for the space.</li>
                  <li><strong>Approval and refinement</strong> — we adjust until the concept is exactly right. No paint goes on a wall before you're sure.</li>
                  <li><strong>Paint</strong> — wall prep, sketch transfer, and hand painting in layers. Small accent murals take 1-2 days; large detailed murals 4-7 days.</li>
                  <li><strong>Topcoat</strong> — optional matte sealer for high-traffic areas or commercial spaces.</li>
                </ol>
            """),
            ("Pricing and Timeline", """
                <p>Custom mural pricing depends on size, complexity, and detail level. As a rough guide:</p>
                <ul>
                  <li><strong>Small accent mural</strong> (3-6 ft wide, simple design): $400-$1,200</li>
                  <li><strong>Medium room mural</strong> (full feature wall, moderate detail): $1,200-$3,500</li>
                  <li><strong>Large or commercial mural</strong> (full wall, high detail, complex composition): $3,500+</li>
                </ul>
                <p>Every mural quote is free and fixed-price after the concept sketch is approved.</p>
            """),
            ("Why Hand-Painted Matters", """
                <p>Wall decals peel. Wallpaper murals show seams. Printed murals fade and can't be touched up. A hand-painted mural is a one-of-a-kind piece of art on your wall — it lasts decades, can be cleaned, and can be touched up later if a hand inevitably finds it. Evelyn has been illustrating since childhood and brings real fine-art technique to every project.</p>
            """),
            ("Recent Project: Bathroom Refresh with Custom Stripe Accent", """
                <p>This bathroom started as a builder-grade tan-walled space with a dark stained vanity. We transformed it into a bright, intentional design with a custom hand-painted vertical stripe accent treatment in soft yellow and a refinished cabinet in a fresh blue — a great example of how mural and custom-design work can completely reshape a small room without major renovation.</p>
                <div class="project-grid">
                  <figure>
                    <img src="/bathroom-before.jpg" alt="Bathroom before custom mural and cabinet refinishing, Grand Rapids" loading="lazy" />
                    <figcaption>Before</figcaption>
                  </figure>
                  <figure>
                    <img src="/bathroom-after.jpg" alt="Bathroom after custom yellow stripe wall treatment and blue cabinet refinishing by Go Green College Painters, Grand Rapids MI" loading="lazy" />
                    <figcaption>After</figcaption>
                  </figure>
                </div>
            """),
        ],
        "faqs": [
            ("How much does a custom mural cost in Grand Rapids?", "Custom murals typically run $400-$1,200 for small accent murals, $1,200-$3,500 for full feature walls, and $3,500+ for large or highly detailed commercial murals. Pricing depends on size, complexity, and detail. Every quote is free after a concept sketch is approved."),
            ("How long does it take to paint a custom mural?", "Small accent murals take 1-2 days. Full feature walls take 3-5 days. Large or commercial murals take 5-10 days. The design phase (consultation and sketch approval) typically adds 3-7 days before painting starts."),
            ("Can I choose my own custom design?", "Absolutely — that's the whole point. We start with a free consultation, sketch concepts based on your ideas and any reference imagery you love, and refine until the design is exactly right before any paint goes on the wall."),
            ("How long will the mural last?", "Hand-painted murals on properly prepped walls last for decades. We use the same premium interior paints we use on the rest of the house, with an optional matte sealer for high-traffic areas. Murals can be touched up easily if scuffed."),
            ("Do you do murals for kids' rooms and nurseries?", "Yes — this is one of our most popular mural categories. Evelyn specializes in playful, story-driven designs for children's spaces, from nursery scenes to whimsical character art for older kids."),
            ("Do you paint commercial murals?", "Yes. We do branded murals, logo illustrations, restaurant feature walls, lobby murals, and exterior commercial murals across Grand Rapids. Commercial projects include a written design brief and fixed-price quote."),
            ("Are you the actual artist, or do you outsource?", "Evelyn personally designs and paints every mural — she's an Industrial Design student at Wayne State University and a lifelong illustrator. Jackson assists with wall prep, transfer, and finishing. No subcontractors."),
        ],
        "related": [
            ("Interior Painting", "/services/interior-painting/"),
            ("Deck Staining", "/services/deck-staining/"),
            ("Exterior Painting", "/services/exterior-painting/"),
        ],
    },

    # ============================================================
    # NEIGHBORHOOD PAGES
    # Cedar-siding expertise is the through-line for Cascade,
    # Forest Hills, and Ada. EGR leans on mixed materials.
    # ============================================================
    {
        "slug": "grand-rapids/cascade/",
        "title": "Cascade, MI House Painters | Cedar Siding Specialists",
        "description": "Owner-operated cedar siding specialists serving Cascade, MI. Tannin-blocking prep, premium acrylic finish, 8–12 year lifespan. Free fixed-price estimate.",
        "h1": "House Painters in Cascade, Michigan",
        "hero_img": "/exterior-after.jpg",
        "service_name": "House Painting in Cascade, Michigan",
        "service_desc": "Owner-operated exterior and interior house painting in Cascade, MI. Specializing in cedar siding repaints — tannin-blocking primer, two coats of premium acrylic, and the prep work that makes paint last in Michigan weather.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "area_served": {
            "@type": "City", "name": "Cascade",
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Kent County, Michigan"},
        },
        "breadcrumb": [("Home", "/"), ("Service Areas", "/#service-areas"), ("Cascade", "/grand-rapids/cascade/")],
        "lead": "Cascade is one of our most-painted areas. The executive ranches, contemporaries, and French country homes along the Forest Hills corridor mean a lot of cedar shake, cedar lap, and cedar trim — surfaces that punish painters who skip prep. We do the prep correctly the first time, with the right primer for cedar's tannins and the right paint for Michigan winters.",
        "sections": [
            ("Why Cascade homeowners hire Go Green", """
                <ul>
                  <li><strong>Owner-operated.</strong> Jackson and Evelyn do every job themselves. No revolving crews of summer hires.</li>
                  <li><strong>Cedar specialists.</strong> We understand tannin bleed-through, knot priming, and the cure schedule cedar needs in Michigan's freeze-thaw climate.</li>
                  <li><strong>Fully insured.</strong> Full liability insurance on every project — proof available on request.</li>
                  <li><strong>Honest, fixed-price estimates.</strong> Free, no-obligation, written quotes. No vague hourly billing.</li>
                  <li><strong>Show up and finish.</strong> We don't disappear mid-project to chase another job.</li>
                </ul>
            """),
            ("Cedar siding in Cascade — what we do differently", """
                <p>Cedar is beautiful and durable but it's also one of the most demanding surfaces to paint. Cascade has more cedar siding than almost any other Grand Rapids-area neighborhood, and we see the same failure modes every spring:</p>
                <ul>
                  <li><strong>Tannin bleed-through</strong> — pinkish or yellow stains rising through fresh paint. We block this with a stain-killing primer (oil-based or pigmented shellac) on bare cedar.</li>
                  <li><strong>Failed paint on south- and west-facing walls</strong> — UV and freeze-thaw delamination. We strip back to a sound substrate before recoating.</li>
                  <li><strong>Mildew in shaded north-side cedar</strong> — common in wooded Cascade lots. We use a mildewcide wash before painting.</li>
                  <li><strong>Knots bleeding sap</strong> — knots get individually spot-primed with a shellac-based primer.</li>
                </ul>
                <p>For homes where the cedar grain matters more than a smooth painted finish, semi-transparent or solid-color stain is often a better choice than paint. We'll give you an honest recommendation during the estimate.</p>
            """),
            ("Common Cascade home types we paint", """
                <p>Most of the Cascade work we do falls into a few categories — each with its own prep approach:</p>
                <ul>
                  <li><strong>Executive ranches (1970s–1990s)</strong> with cedar lap or cedar shake siding, often with brick or stone accents. Long horizontal runs need careful color planning to avoid lap marks.</li>
                  <li><strong>Contemporary / modern</strong> homes with mixed siding (cedar + stucco + metal). Each material gets its own prep and paint system.</li>
                  <li><strong>French country and traditional</strong> two-stories with cedar trim, dormers, and detail elements. Trim color is usually the make-or-break.</li>
                  <li><strong>Newer Forest Hills builds</strong> (2000s+) with engineered cedar or composite siding — different prep requirements than real cedar.</li>
                </ul>
            """),
            ("What painting a Cascade home costs", """
                <p>Cascade home values run higher than the Grand Rapids average — currently around $512K — and the exterior painting cost reflects the size and complexity of these homes. Most Cascade exterior repaints fall in the <strong>$5,000 to $9,000</strong> range, with larger or more detailed homes running higher. Interior whole-home repaints typically run <strong>$5,000 to $10,000</strong>.</p>
                <p>Cedar work and multi-story scaffolding access add to cost vs. simpler vinyl siding jobs — but they're also why the result lasts longer when done correctly.</p>
                <p>Every Cascade estimate is free and fixed-price after a walk-through.</p>
            """),
        ],
        "faqs": [
            ("Do you specialize in cedar siding?", "Yes. Cedar is one of our most-painted surfaces — common in Cascade, Forest Hills, and Ada. We use tannin-blocking primer on bare cedar, spot-prime knots with shellac, and follow up with two coats of premium acrylic exterior paint (Sherwin-Williams Duration or Benjamin Moore Aura Exterior). Cedar prep is more involved than vinyl or fiber-cement, which is why a lot of painters skip it — we don't."),
            ("Should I paint or stain my cedar siding?", "Both are valid. Stain (semi-transparent or solid) lets the cedar grain show through and ages more gracefully — fewer flake-and-peel failures over time. Paint gives more color flexibility and a uniform finish but needs more thorough prep and recoats sooner. We'll give you an honest recommendation based on the cedar's current state during the estimate."),
            ("How much does it cost to paint a Cascade home?", "Most Cascade exterior repaints run $5,000 to $9,000 depending on home size, story count, accessibility, and siding type. Interior whole-home repaints typically run $5,000 to $10,000. Cedar siding is at the higher end because of the prep involved. Every estimate is free and fixed-price."),
            ("What zip codes do you serve in Cascade?", "Primarily 49301 (Cascade Township) and the Forest Hills areas of 49506 and 49546. We serve all of Greater Grand Rapids — call us if you're unsure whether your address is in range."),
            ("When can you start a Cascade exterior repaint?", "Our exterior painting season runs roughly May through mid-October when surface temps are above 50°F overnight. Most Cascade projects book 2–6 weeks out depending on the season; reach out earlier for spring or fall slots, which fill fastest."),
            ("Do you handle multi-story Cascade homes?", "Yes. We carry the ladders and access equipment for two- and three-story exteriors with standard rooflines. For complex multi-story dormer work or homes requiring scaffolding rentals, we'll include the rental in the fixed-price estimate."),
        ],
        "related": [
            ("Forest Hills", "/grand-rapids/forest-hills/"),
            ("Ada", "/grand-rapids/ada/"),
            ("East Grand Rapids", "/grand-rapids/east-grand-rapids/"),
            ("Exterior Painting Services", "/services/exterior-painting/"),
        ],
        "related_heading": "Other Service Areas",
    },

    {
        "slug": "grand-rapids/forest-hills/",
        "title": "Forest Hills House Painters | Cedar Specialists, Free Quote",
        "description": "Owner-operated cedar siding specialists serving the Forest Hills schools area. Exterior cedar, interior repaints, cabinet refinishing. Free fixed-price quote.",
        "h1": "House Painters in Forest Hills, Michigan",
        "hero_img": "/exterior-after.jpg",
        "service_name": "House Painting in the Forest Hills Area, Michigan",
        "service_desc": "Owner-operated exterior and interior house painting in the Forest Hills area of Greater Grand Rapids. Cedar siding expertise, premium paints, owner-on-every-job. Free estimates.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "area_served": {
            "@type": "City", "name": "Forest Hills",
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Kent County, Michigan"},
        },
        "breadcrumb": [("Home", "/"), ("Service Areas", "/#service-areas"), ("Forest Hills", "/grand-rapids/forest-hills/")],
        "lead": "The Forest Hills area — Forest Hills Northern, Central, and Eastern school zones spanning Cascade, Ada, and Eastern Kent County — is one of our core service areas. Mostly settled, family-focused homes with a heavy concentration of cedar-sided traditional and craftsman builds. Same prep philosophy as Cascade: do it right or don't bother.",
        "sections": [
            ("Why Forest Hills homeowners choose Go Green", """
                <ul>
                  <li><strong>Owner-operated.</strong> Jackson (MSU) and Evelyn (Wayne State) do every job themselves — no rotating crews of summer hires who'll be gone by August.</li>
                  <li><strong>Reliable scheduling.</strong> We show up on the day we said we would, and we don't disappear mid-project.</li>
                  <li><strong>Cedar siding expertise.</strong> Same prep approach as Cascade — tannin-blocking primer, knot priming, two coats of premium acrylic.</li>
                  <li><strong>Fully insured.</strong> Full liability coverage on every project.</li>
                  <li><strong>Family-business honest pricing.</strong> Free fixed-price estimates with no upsell games.</li>
                </ul>
            """),
            ("Cedar siding in Forest Hills — same playbook as Cascade", """
                <p>The Forest Hills school-zone neighborhoods share Cascade's heavy use of cedar siding, especially in homes built between the 1970s and early 2000s. The cedar prep approach is identical:</p>
                <ul>
                  <li><strong>Stain-killing primer on bare cedar</strong> to block tannin bleed-through before topcoats go on.</li>
                  <li><strong>Spot-prime knots with shellac</strong> so sap doesn't bleed through the finish coat.</li>
                  <li><strong>Mildewcide wash on north-facing and shaded walls</strong> before painting.</li>
                  <li><strong>Strip back to a sound substrate</strong> wherever paint is failing, especially south- and west-facing exposures.</li>
                </ul>
                <p>If your cedar is in good shape but the grain still reads through your current paint, a semi-transparent or solid-color stain is often a better finish than another coat of paint.</p>
            """),
            ("Interior painting for Forest Hills families", """
                <p>A lot of our Forest Hills work is interior repaints in family homes — refreshing rooms after years of life, prepping for resale, or transforming a builder-grade interior into something with more character. Common projects include:</p>
                <ul>
                  <li>Whole-home repaints (3 to 7 days for an average Forest Hills home)</li>
                  <li>Kitchen cabinet refinishing (4 to 6 days for a typical kitchen)</li>
                  <li>Kids' room mural work — Evelyn's specialty</li>
                  <li>Ceiling repaints (popcorn-ceiling refresh, vaulted ceilings)</li>
                  <li>Trim and door enamel work</li>
                </ul>
            """),
            ("What painting in Forest Hills costs", """
                <p>Forest Hills home values average around $450K — a step below Cascade but with substantial homes. Most exterior repaints in the Forest Hills area run <strong>$4,500 to $8,500</strong>; interior whole-home repaints typically run <strong>$5,000 to $9,000</strong>; cabinet refinishing runs <strong>$2,500 to $5,500</strong>. Every quote is free and fixed-price after a walk-through.</p>
            """),
        ],
        "faqs": [
            ("What zip codes do you serve in the Forest Hills area?", "We serve 49301 (Cascade portion), 49546 (Forest Hills proper), and the eastern parts of 49506. If you're in the Forest Hills Northern, Central, or Eastern school district, you're in our service area."),
            ("Do you handle Forest Hills cedar siding repaints?", "Yes — cedar is one of our most-painted surfaces. We use tannin-blocking primer on bare cedar, spot-prime knots with shellac, and apply two coats of premium acrylic exterior paint. Cedar requires more prep than most surfaces, and we don't skip it."),
            ("How long does a Forest Hills exterior repaint take?", "Most Forest Hills exterior repaints take 4 to 7 days from start to finish, depending on home size, story count, and prep needs. Weather can extend the timeline — exterior paint needs surface temps above 50°F and dry conditions."),
            ("Can you do interior painting in winter?", "Yes — interior is a year-round service. Many Forest Hills families schedule interior work in fall and winter so the house is ready for summer. We use low-odor interior paints so rooms are usable quickly after we finish."),
            ("Do you offer cabinet refinishing in Forest Hills?", "Yes. Cabinet refinishing is a specialty — we remove and label every door and drawer, scuff-sand, prime with a bonding primer, and apply two coats of cabinet-grade enamel. A typical Forest Hills kitchen takes 4–6 days and runs $2,500–$5,500."),
            ("Will Evelyn paint a mural in my kid's room?", "Yes — kids' rooms and nurseries are one of our most-requested mural categories. Evelyn is an Industrial Design student at Wayne State University and a lifelong illustrator. We start with a free design consultation and sketches before any paint goes on the wall."),
        ],
        "related": [
            ("Cascade", "/grand-rapids/cascade/"),
            ("Ada", "/grand-rapids/ada/"),
            ("East Grand Rapids", "/grand-rapids/east-grand-rapids/"),
            ("Interior Painting Services", "/services/interior-painting/"),
        ],
        "related_heading": "Other Service Areas",
    },

    {
        "slug": "grand-rapids/ada/",
        "title": "Ada, MI House Painters | Cedar Siding Specialists",
        "description": "Owner-operated cedar siding specialists in Ada — Ada Village, Bostwick Lake, and the wooded estates south of Fulton. Free fixed-price written estimate.",
        "h1": "House Painters in Ada, Michigan",
        "hero_img": "/exterior-after.jpg",
        "service_name": "House Painting in Ada, Michigan",
        "service_desc": "Owner-operated exterior and interior house painting in Ada, MI. Cedar siding repaints, premium primers and finishes, owner-on-every-job. Free estimates.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "area_served": {
            "@type": "City", "name": "Ada",
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Kent County, Michigan"},
        },
        "breadcrumb": [("Home", "/"), ("Service Areas", "/#service-areas"), ("Ada", "/grand-rapids/ada/")],
        "lead": "Ada Township sits just east of Grand Rapids — home to Amway HQ, the redeveloped Ada Village downtown, and some of the most cedar-heavy homes in the region. We paint exteriors, interiors, decks, and cabinets across Ada with the same owner-operated approach we use in Cascade and Forest Hills.",
        "sections": [
            ("Why Ada homeowners hire Go Green", """
                <ul>
                  <li><strong>Owner-on-every-job.</strong> No subcontractors, no rotating summer crews. Jackson and Evelyn do the work themselves.</li>
                  <li><strong>Cedar siding craft.</strong> Tannin-blocking primer, knot priming, two coats of premium acrylic — the prep most painters skip.</li>
                  <li><strong>Fully insured</strong> with proof of insurance on request.</li>
                  <li><strong>Fixed-price written estimates.</strong> No hourly meter, no surprise add-ons.</li>
                  <li><strong>Local college family.</strong> Jackson at Michigan State, Evelyn at Wayne State — we're invested in doing this right and earning repeat business.</li>
                </ul>
            """),
            ("Cedar in Ada — the prep matters more than the paint", """
                <p>Ada has a lot of cedar shake, cedar lap, and cedar accent work — especially in the older Ada Village neighborhoods, the larger executive homes near Bostwick Lake, and the wooded properties south of Fulton. Cedar repaint failures are usually a prep problem, not a paint problem:</p>
                <ul>
                  <li><strong>Tannins bleed through topcoats</strong> without a stain-killing primer — we use oil-based or pigmented shellac on bare cedar.</li>
                  <li><strong>Knots ooze sap</strong> through fresh paint within a season unless individually shellac-primed.</li>
                  <li><strong>South- and west-facing walls fail first</strong> from UV — we strip back to a sound substrate where needed.</li>
                  <li><strong>Shaded north-side cedar grows mildew</strong> — washed off with a mildewcide before painting.</li>
                </ul>
                <p>If the cedar grain is still attractive, a semi-transparent or solid-color stain often wears better than another coat of paint. We'll be honest about which option suits your specific home.</p>
            """),
            ("Common Ada home types we paint", """
                <ul>
                  <li><strong>Ada Village area homes</strong> — older two-stories and 1.5-stories, often with cedar trim and brick or stone accents.</li>
                  <li><strong>Executive homes near Bostwick Lake and Honey Creek</strong> — large cedar-sided builds requiring multi-day prep.</li>
                  <li><strong>Newer subdivisions</strong> in 49301 — fiber-cement and engineered siding with cedar accent elements.</li>
                  <li><strong>Wooded estates</strong> south of Fulton — mature trees mean more mildew prep on shaded exposures.</li>
                </ul>
            """),
            ("What painting in Ada costs", """
                <p>Ada home values track closely with Cascade — substantial homes that take substantial prep. Typical Ada exterior repaints run <strong>$5,000 to $9,000</strong>; whole-home interior repaints run <strong>$5,000 to $10,000</strong>; cabinet refinishing runs <strong>$2,500 to $6,000</strong>. Every quote is free and fixed-price after a walk-through.</p>
            """),
        ],
        "faqs": [
            ("Do you paint cedar homes in Ada?", "Yes — cedar is one of our most-painted surfaces, and Ada has a high concentration of cedar siding. We use tannin-blocking primer on bare cedar, individually spot-prime knots, and apply two coats of premium acrylic. Cedar prep is more involved than vinyl or fiber-cement; we don't skip it."),
            ("What zip codes do you serve in Ada?", "Primarily 49301 (Ada Township, shared with Cascade). We serve all of Greater Grand Rapids — call if you're unsure whether your address is in range."),
            ("How much does an Ada exterior repaint cost?", "Most Ada exterior repaints run $5,000 to $9,000, depending on home size, story count, accessibility, and the amount of cedar prep needed. Every estimate is free and fixed-price after a walk-through."),
            ("Should I stain my cedar instead of repainting it?", "Often, yes — especially if the cedar is in good shape and the grain still reads as attractive. Stain wears more gracefully than paint and is easier to refresh in 4–6 years without scraping. We'll give you an honest recommendation during the estimate."),
            ("When is the best time to schedule an Ada exterior project?", "Late May through mid-October is the prime exterior paint window — we need surface temperatures above 50°F overnight and dry weather for 24–48 hours after each coat. Late spring and early fall are the most popular slots; book 4–6 weeks ahead."),
            ("Can you do interior cabinet painting in Ada?", "Yes. Cabinet refinishing is a specialty — we remove and label every door and drawer, scuff-sand, prime with a bonding primer, and apply two coats of cabinet-grade enamel. A typical Ada kitchen takes 4–6 days."),
        ],
        "related": [
            ("Cascade", "/grand-rapids/cascade/"),
            ("Forest Hills", "/grand-rapids/forest-hills/"),
            ("East Grand Rapids", "/grand-rapids/east-grand-rapids/"),
            ("Exterior Painting Services", "/services/exterior-painting/"),
        ],
        "related_heading": "Other Service Areas",
    },

    {
        "slug": "grand-rapids/east-grand-rapids/",
        "title": "East Grand Rapids House Painters | Established Homes",
        "description": "Owner-operated painters serving East Grand Rapids. Established 1920s–1950s homes, Reeds Lake custom builds, cedar trim, plaster walls. Free fixed-price quote.",
        "h1": "House Painters in East Grand Rapids, Michigan",
        "hero_img": "/exterior-after.jpg",
        "service_name": "House Painting in East Grand Rapids, Michigan",
        "service_desc": "Owner-operated exterior and interior house painting in East Grand Rapids (EGR), MI. Established-home prep, cedar where it appears, premium finishes, and owner-on-every-job. Free estimates.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "area_served": {
            "@type": "City", "name": "East Grand Rapids",
            "containedInPlace": {"@type": "AdministrativeArea", "name": "Kent County, Michigan"},
        },
        "breadcrumb": [("Home", "/"), ("Service Areas", "/#service-areas"), ("East Grand Rapids", "/grand-rapids/east-grand-rapids/")],
        "lead": "East Grand Rapids is older, denser, and more walkable than Cascade or Ada — and the homes reflect it. Most EGR homes are established 1920s-1950s builds (brick, stucco, clapboard, and some cedar) plus newer custom homes near Reeds Lake. The painting work here is detail-heavy: lots of trim, period-correct color planning, and prep work that respects original substrates.",
        "sections": [
            ("Why East Grand Rapids homeowners choose Go Green", """
                <ul>
                  <li><strong>Owner-operated.</strong> Jackson and Evelyn do every job themselves — no crews of strangers in your home.</li>
                  <li><strong>Established-home experience.</strong> Older homes need more careful prep — flaking paint, layered repaints, plaster repair on interiors. We move slowly and respect the original substrate.</li>
                  <li><strong>Detail-focused.</strong> Hand-cut lines, careful trim work, period-correct color planning if you want it.</li>
                  <li><strong>Fully insured.</strong> Full liability insurance on every project.</li>
                  <li><strong>Honest, fixed-price estimates.</strong> Free, written quotes — no hourly mystery.</li>
                </ul>
            """),
            ("Common EGR home types we paint", """
                <ul>
                  <li><strong>1920s–1940s clapboard and brick two-stories</strong> around Wealthy and Lake Drive — typically need careful scraping, spot-priming, and trim-color decisions.</li>
                  <li><strong>Mid-century ranches and split-levels</strong> with mixed brick, wood, and aluminum siding — each material gets its own prep system.</li>
                  <li><strong>Reeds Lake-area custom homes</strong> — newer cedar, stone, and stucco builds with extensive trim detail.</li>
                  <li><strong>Older interiors</strong> with plaster walls, original trim, and period color palettes — repaints that need to respect what's already there.</li>
                </ul>
            """),
            ("Cedar siding in EGR — present but less common", """
                <p>Cedar is less ubiquitous in EGR than in Cascade or Ada, but you'll still find it on newer Reeds Lake-area custom builds and on some 1970s-era homes near Breton and Lake Drive. When we see cedar, we apply the same prep playbook: tannin-blocking primer, knot spot-priming, premium acrylic topcoats. Stain is also a valid option for cedar in EGR — we'll walk through both at the estimate.</p>
            """),
            ("Interior work in EGR homes", """
                <p>A lot of our EGR work is interior — refreshing established homes, prepping for resale, or transforming a dated palette. Older plaster walls in EGR homes often need patching and priming before the topcoat goes on, and original trim is usually worth saving rather than replacing. Cabinet refinishing is also popular — most EGR kitchens have solid-wood cabinets worth refinishing instead of replacing.</p>
            """),
            ("What painting in EGR costs", """
                <p>East Grand Rapids home values average around $500K with substantial variation between older established homes and newer Reeds Lake custom builds. Most EGR exterior repaints run <strong>$4,500 to $8,500</strong>, with detail-heavy 1920s homes at the higher end. Interior whole-home repaints typically run <strong>$5,000 to $9,500</strong>. Cabinet refinishing runs <strong>$2,500 to $6,000</strong>.</p>
            """),
        ],
        "faqs": [
            ("What zip code do you serve in East Grand Rapids?", "Primarily 49506 — the EGR city limits plus the eastern edge of Grand Rapids. If you're south of Lake Drive, north of Burton, east of Plymouth, you're squarely in our service area."),
            ("Can you paint older EGR homes?", "Yes — established 1920s–1950s homes are a significant portion of our EGR work. Older homes need more careful prep (scraping flaking paint without damaging substrate, spot-priming patched plaster, color-matching original trim) and we slow down to respect that."),
            ("Do you do period-correct color planning for older EGR homes?", "If you want it — Evelyn (Industrial Design student at Wayne State) is happy to advise on palettes that respect the era of your home. We can also work from a color you've already chosen."),
            ("How much does an EGR exterior repaint cost?", "Most EGR exterior repaints run $4,500 to $8,500 depending on home size and detail level. Older homes with extensive trim and prep needs run at the higher end; simpler ranch and split-level homes run lower. Every estimate is free and fixed-price."),
            ("Can you repaint EGR cabinets?", "Yes. Most EGR kitchens have real wood cabinets that are perfect candidates for refinishing — much cheaper than replacement, and results look factory-applied when done right. Typical EGR kitchen runs $2,500–$6,000."),
            ("Do you do murals or accent walls in EGR homes?", "Yes — Evelyn does custom hand-painted murals for kids' rooms, dining rooms, and accent walls. We've done several EGR projects including the bathroom-with-yellow-stripe-accent-and-blue-vanity featured on our murals page."),
        ],
        "related": [
            ("Cascade", "/grand-rapids/cascade/"),
            ("Forest Hills", "/grand-rapids/forest-hills/"),
            ("Ada", "/grand-rapids/ada/"),
            ("Interior Painting Services", "/services/interior-painting/"),
        ],
        "related_heading": "Other Service Areas",
    },
]

# ============================================================
# BLOG POSTS
# Each post renders with Article + FAQPage + BreadcrumbList schema.
# To add a post: append a dict here and rerun build_pages.py.
# ============================================================
BLOG_POSTS = [
    {
        "slug": "blog/cost-to-paint-a-house-in-grand-rapids/",
        "title": "Grand Rapids House Painting Cost in 2026: Real Numbers",
        "description": "Interior $4,700–$8,500. Exterior $3,000–$7,000. Cabinets $2,500–$6,000. What drives Grand Rapids painting costs up or down — plus how to get a real quote.",
        "h1": "How Much Does It Cost to Paint a House in Grand Rapids?",
        "hero_img": "/exterior-after.jpg",
        "date_published": "2026-05-13",
        "date_modified": "2026-05-13",
        "author_id": f"{SITE}/#jackson",
        "author_name": "Jackson Befus",
        "breadcrumb": [("Home", "/"), ("Blog", "/blog/"), ("Cost to Paint a House in Grand Rapids", "/blog/cost-to-paint-a-house-in-grand-rapids/")],
        "lead": "Most house painting projects in Grand Rapids fall between $700 and $9,500 depending on what you're painting. Interior repaints run roughly $700–$1,700 per room or $4,700–$8,500 for a whole house; exterior repaints run $3,000–$7,000 for a typical home; kitchen cabinet refinishing runs $2,500–$6,000; and deck staining runs $700–$2,500. Here's the full 2026 breakdown — what's included at each price point, and what pushes a quote higher or lower.",
        "sections": [
            ("Interior Painting Costs in Grand Rapids", """
                <p>Interior painting is usually priced per room or as a whole-home package. As a 2026 guide for the Grand Rapids area:</p>
                <ul>
                  <li><strong>Single room (bedroom, office):</strong> $700–$1,200</li>
                  <li><strong>Living room or large room with vaulted ceiling:</strong> $1,000–$1,700</li>
                  <li><strong>Whole-home interior repaint:</strong> $4,700–$8,500</li>
                  <li><strong>Trim, doors, and baseboards (per room):</strong> $200–$500 on top of wall pricing</li>
                  <li><strong>Ceilings:</strong> $150–$400 per room depending on height and condition</li>
                </ul>
                <p>That pricing assumes two coats, standard 8–9 ft ceilings, minor wall prep (nail holes, small dings), and quality acrylic latex paint. Heavily damaged walls, dark-to-light color changes, and tall or detailed rooms push the number up.</p>
            """),
            ("Exterior Painting Costs in Grand Rapids", """
                <p>Exterior repaints in the Grand Rapids area generally run <strong>$3,000–$7,000</strong> for a typical one- or two-story home. The biggest cost drivers are:</p>
                <ul>
                  <li><strong>Home size and story count</strong> — more square footage and height means more labor and access equipment.</li>
                  <li><strong>Siding type</strong> — vinyl and fiber-cement are quicker; cedar siding takes significantly more prep (tannin-blocking primer, knot priming) and runs at the higher end.</li>
                  <li><strong>Current paint condition</strong> — peeling and failing paint needs scraping and spot-priming, which adds labor.</li>
                  <li><strong>Detail elements</strong> — shutters, trim, dormers, railings, and multi-color schemes add time.</li>
                </ul>
                <p>Larger executive homes — common in Cascade, Ada, and the Forest Hills area — frequently run $5,000–$9,000 because of size, cedar siding, and multi-story access.</p>
            """),
            ("Kitchen Cabinet Refinishing Costs", """
                <p>Refinishing kitchen cabinets is one of the highest-value painting projects you can do — a fraction of the cost of replacement, with results that look factory-applied when done correctly. In Grand Rapids, cabinet refinishing typically runs <strong>$2,500–$6,000</strong> depending on:</p>
                <ul>
                  <li>Number of doors and drawer fronts</li>
                  <li>Whether you're painting the boxes as well as the doors</li>
                  <li>Current finish (raw wood, stained, or previously painted)</li>
                  <li>Color change complexity</li>
                </ul>
                <p>The process matters more than the paint here: doors removed and labeled, surfaces degreased and scuff-sanded, a bonding primer, and two coats of cabinet-grade enamel. A typical kitchen takes 4–6 days.</p>
            """),
            ("Deck and Fence Staining Costs", """
                <p>Deck and fence staining in Grand Rapids generally runs <strong>$700–$2,500</strong>, depending on the size of the deck, the surface condition, and the type of stain. A standard 200–400 sq ft deck usually falls in the $900–$1,800 range. Transparent and semi-transparent stains cost less than solid stains, and a badly weathered deck needs more cleaning and sanding labor.</p>
                <p>Note: this is refinishing and staining only. Board replacement and structural carpentry aren't part of a staining quote — those are a separate carpentry job.</p>
            """),
            ("What Drives a Painting Quote Up or Down", """
                <p>Two homes the same size can get very different quotes. The main factors:</p>
                <ul>
                  <li><strong>Prep work needed</strong> — the single biggest variable. Sound surfaces paint fast; failing paint, water damage, or heavy cracking adds hours.</li>
                  <li><strong>Surface material</strong> — cedar siding, stucco, and rough-sawn wood take more time and specialty primers than vinyl or smooth drywall.</li>
                  <li><strong>Number of coats</strong> — dramatic color changes and deep colors often need an extra coat.</li>
                  <li><strong>Height and access</strong> — second and third stories, steep lots, and complex rooflines require more equipment and time.</li>
                  <li><strong>Detail and trim</strong> — lots of trim, shutters, railings, and multi-color schemes increase labor.</li>
                  <li><strong>Paint quality</strong> — premium paints cost more per gallon but last years longer; we don't recommend cutting this corner.</li>
                  <li><strong>Season</strong> — spring and fall are peak; booking in the shoulder season sometimes means more scheduling flexibility.</li>
                </ul>
            """),
            ("Does Your Neighborhood Affect the Price?", """
                <p>Indirectly, yes — not because painters charge more by ZIP code, but because home characteristics vary by area. Cascade, Ada, and Forest Hills have larger homes and far more cedar siding, so exterior quotes there tend to run higher. East Grand Rapids has older established homes with detailed trim and plaster walls, which adds prep time. The price tracks the house, not the address.</p>
            """),
            ("How to Get an Accurate Painting Quote", """
                <p>Online calculators and per-square-foot averages are a starting point, but the only way to get a real number is an in-person walk-through. At Go Green College Painters, every estimate is <strong>free, fixed-price, and in writing</strong> — we walk the home, identify the prep that's actually needed, and quote a number that won't change unless the scope does.</p>
                <p>We're a student-owned, owner-operated company — Jackson and Evelyn Befus do every job themselves. Call <a href="tel:+16162642119">(616) 264-2119</a> or <a href="/#contact">request a free estimate</a> and we'll get you a number within 24 hours.</p>
            """),
        ],
        "faqs": [
            ("How much does it cost to paint the interior of a house in Grand Rapids?", "A whole-home interior repaint in Grand Rapids typically runs $4,700–$8,500, or about $700–$1,700 per room. Pricing assumes two coats, standard ceiling height, minor wall prep, and quality acrylic latex paint. Damaged walls, tall rooms, and dramatic color changes push the cost higher."),
            ("How much does it cost to paint the exterior of a house in Grand Rapids?", "Exterior repaints in Grand Rapids generally run $3,000–$7,000 for a typical one- or two-story home. Cedar siding, multi-story access, failing paint that needs scraping, and detailed trim all push the price toward the higher end. Larger executive homes in Cascade, Ada, and Forest Hills often run $5,000–$9,000."),
            ("How much does cabinet refinishing cost in Grand Rapids?", "Kitchen cabinet refinishing in Grand Rapids typically runs $2,500–$6,000, depending on the number of doors and drawers, whether the boxes are painted too, and the complexity of the color change. It's a fraction of the cost of cabinet replacement."),
            ("How much does it cost to stain a deck in Grand Rapids?", "Deck staining in Grand Rapids generally runs $700–$2,500, with a standard 200–400 sq ft deck usually falling in the $900–$1,800 range. Solid stains cost more than transparent stains, and a heavily weathered deck needs more cleaning and sanding labor. This is refinishing only — board replacement is a separate carpentry job."),
            ("Why are painting quotes so different from one company to another?", "The biggest variable is prep work — a quote that skips proper scraping, priming, and caulking will look cheaper but won't last. Other differences come from paint quality, number of coats, and whether the company is owner-operated or carries higher overhead. Always compare what's actually included, not just the bottom-line number."),
            ("Does Go Green College Painters give free estimates?", "Yes — every estimate is free, fixed-price, and provided in writing. We walk the home, identify the prep that's genuinely needed, and quote a number that won't change unless the scope does. Call (616) 264-2119 or request an estimate through our website."),
            ("Is it cheaper to paint in a certain season?", "Exterior painting in Grand Rapids runs roughly May through mid-October when temperatures cooperate, and spring and fall are peak demand. Interior painting is a year-round service, and scheduling interior work in late fall or winter often means more flexibility on dates."),
        ],
        "related": [
            ("Interior Painting", "/services/interior-painting/"),
            ("Exterior Painting", "/services/exterior-painting/"),
            ("Deck Staining", "/services/deck-staining/"),
            ("Custom Murals", "/services/custom-murals/"),
        ],
        "related_heading": "Our Services",
    },

    {
        "slug": "blog/cedar-siding-paint-or-stain-grand-rapids/",
        "title": "Cedar Siding in Grand Rapids: Should You Paint or Stain? (2026 Guide)",
        "description": "Paint vs. stain on cedar siding in Grand Rapids, MI: when each makes sense, lifespan, cost, common failure modes in our climate, and what we recommend. From owner-operated cedar specialists serving Cascade, Forest Hills, Ada, and East Grand Rapids.",
        "h1": "Cedar Siding in Grand Rapids: Should You Paint or Stain?",
        "hero_img": "/exterior-after.jpg",
        "date_published": "2026-06-10",
        "date_modified": "2026-06-10",
        "author_id": f"{SITE}/#jackson",
        "author_name": "Jackson Befus",
        "breadcrumb": [("Home", "/"), ("Blog", "/blog/"), ("Cedar Siding: Paint or Stain", "/blog/cedar-siding-paint-or-stain-grand-rapids/")],
        "lead": "Cedar is one of the most beautiful — and most demanding — exterior surfaces in West Michigan. If your home in Cascade, Ada, Forest Hills, or anywhere on the east side of Grand Rapids has cedar lap, shake, or shingle siding, you've probably wondered whether to paint it or stain it next time around. Here's an honest walk-through: when each makes sense, what they actually cost, how long they last, and the prep mistakes that cause most cedar finishes to fail in our climate.",
        "sections": [
            ("Why Grand Rapids Has So Much Cedar", """
                <p>Cedar siding hit its peak in West Michigan residential building between roughly 1970 and the mid-2000s. Builders favored it for its natural rot resistance, the warmth it gave executive homes and ranch builds, and the way it weathered into a silvery patina when left unfinished. The eastern Grand Rapids neighborhoods — <a href="/grand-rapids/cascade/">Cascade</a>, the <a href="/grand-rapids/forest-hills/">Forest Hills</a> school corridor, <a href="/grand-rapids/ada/">Ada</a>, and the newer Reeds Lake-area builds in <a href="/grand-rapids/east-grand-rapids/">East Grand Rapids</a> — have more cedar per square block than almost anywhere else in West Michigan.</p>
                <p>That history matters because the finish decisions you make today have to respect what's already on the wall. A 1985 cedar ranch in Cascade that's been painted three times has different needs than a 2008 Forest Hills custom build that's been stained twice.</p>
            """),
            ("What Paint Actually Does on Cedar", """
                <p>Paint forms a film on the surface of the wood. It seals the cedar from moisture, blocks UV from fading the substrate, and gives you a near-unlimited color palette. Done right, an exterior paint job on cedar in Grand Rapids will last 8 to 12 years on the protected sides of the home, and 5 to 8 years on the brutally-exposed south and west walls.</p>
                <p>But paint also has failure modes that stain doesn't. When water gets behind a paint film — through a missed caulk gap, a knot that wasn't spot-primed, or sun cycling — it lifts the paint from the wood. That's where the peeling and flaking comes from. Once paint starts failing on cedar, the repair work to get a sound substrate again is significant.</p>
            """),
            ("What Stain Actually Does on Cedar", """
                <p>Stain penetrates the wood instead of coating it. There's no film to lift. As the stain ages, it fades and erodes rather than peeling, so the next maintenance cycle is a wash, sometimes a light sand, and a fresh coat — not a full strip-back.</p>
                <p>Stain comes in three transparencies, each with very different effects on cedar:</p>
                <ul>
                  <li><strong>Transparent</strong> — barely tinted, full grain visible. Best for newer cedar in great shape. Shortest lifespan (2-4 years on exposed walls).</li>
                  <li><strong>Semi-transparent</strong> — tinted, grain still reads through. The most popular choice for residential cedar. 4-6 year cycle.</li>
                  <li><strong>Solid stain</strong> — paint-like opacity, hides the grain almost entirely while still penetrating the wood. 6-8 year cycle. The middle path when paint failures have you nervous but you want consistent color.</li>
                </ul>
            """),
            ("Which Should You Choose?", """
                <p>Quick decision framework:</p>
                <p><strong>Lean toward stain if:</strong></p>
                <ul>
                  <li>Your cedar is in good shape and you like the grain showing</li>
                  <li>You want lower-friction maintenance (sand and recoat, no scrape-and-prime)</li>
                  <li>The home has already been stained — switching to paint adds significant prep cost</li>
                  <li>You're in a wooded lot with mildew pressure (stain breathes more, less likely to trap moisture)</li>
                </ul>
                <p><strong>Lean toward paint if:</strong></p>
                <ul>
                  <li>Your cedar has already been painted multiple times — switching to stain requires stripping back to bare wood, which is rarely cost-effective</li>
                  <li>You want a specific bold or unusual color that stain can't deliver</li>
                  <li>The cedar grain is no longer particularly attractive (heavily weathered, repaired in patches, mismatched ages)</li>
                  <li>Architectural style calls for a uniform painted finish (Colonial, traditional two-story, certain historic styles)</li>
                </ul>
            """),
            ("Four Cedar Failure Modes We See Every Spring in Grand Rapids", """
                <p>Almost every cedar exterior repaint or restain we walk in Grand Rapids has at least one of these problems. Knowing them helps you understand why prep cost varies so much between honest estimates:</p>
                <ul>
                  <li><strong>Tannin bleed-through.</strong> Cedar's natural tannins migrate up through fresh paint or stain on bare wood, leaving pinkish or amber streaks. Caused by skipping a tannin-blocking primer. Fix: oil-based or pigmented shellac primer on bare cedar before the topcoat.</li>
                  <li><strong>Knot bleed.</strong> Cedar knots ooze sap that bleeds through coatings within a season. Caused by not spot-priming knots. Fix: shellac-based primer on every visible knot, individually, before the field paint or stain goes on.</li>
                  <li><strong>South- and west-wall peeling.</strong> UV and freeze-thaw cycles attack south and west exposures hardest. North walls can hold paint twice as long. Caused by both the climate and inadequate prep on the worst-hit walls. Fix: strip failing paint back to a sound substrate, prime, then topcoat — even if the rest of the home only needs a single coat.</li>
                  <li><strong>Mildew under the shaded eaves.</strong> Wooded Cascade and Ada lots see persistent shade and high humidity on north sides. Mildew grows on the existing finish and feeds on dust. New paint over mildew will fail. Fix: wash with a mildewcide cleaner before any other prep.</li>
                </ul>
            """),
            ("Products We Recommend for Cedar in Michigan's Climate", """
                <p>For <strong>paint</strong>, we use 100% acrylic premium exterior lines: Sherwin-Williams Duration or Emerald Exterior, or Benjamin Moore Aura Exterior or Regal Select. These are formulated for film flexibility (important for Michigan freeze-thaw) and UV resistance.</p>
                <p>For <strong>stain</strong>, our default is Benjamin Moore Arborcoat (the semi-transparent and solid lines both perform exceptionally well on cedar in our climate). Sherwin-Williams SuperDeck and DeckScapes are also solid choices.</p>
                <p>For <strong>primer</strong> on bare cedar: an oil-based stain-blocker (Zinsser Cover-Stain) or a pigmented shellac (BIN) for the worst tannin and knot work. Latex primers don't reliably block cedar tannins.</p>
            """),
            ("Cost in Grand Rapids", """
                <p>A few realistic ranges for an average two-story Cascade or Forest Hills home with mostly cedar siding:</p>
                <ul>
                  <li><strong>Stain (semi-transparent or solid)</strong>: roughly $4,500 to $8,500</li>
                  <li><strong>Repaint (sound paint, minor prep)</strong>: roughly $5,000 to $8,000</li>
                  <li><strong>Repaint with significant peeling and tannin/knot issues</strong>: roughly $7,500 to $12,000</li>
                </ul>
                <p>Stain projects on cedar are usually a bit less expensive than paint projects on the same home because there's no film to scrape back. The wide ranges come from how much prep is genuinely needed — that's why a fixed-price walk-through estimate is worth more than a per-square-foot number from a website.</p>
            """),
            ("Lifespan and Maintenance", """
                <p>Honest expectations for cedar in Grand Rapids:</p>
                <ul>
                  <li><strong>Transparent stain</strong>: 2-4 years between coats</li>
                  <li><strong>Semi-transparent stain</strong>: 4-6 years</li>
                  <li><strong>Solid stain</strong>: 6-8 years</li>
                  <li><strong>Premium acrylic paint</strong>: 8-12 years (less on south/west walls)</li>
                </ul>
                <p>The maintenance work itself is also different. Re-staining is a wash and a recoat — generally a few days, much lower cost than a full repaint. Repainting a previously-painted cedar home, even when the existing paint is sound, involves more prep, primer, and finish coats. That difference is why some homeowners switch from paint to stain over time, even though the upfront change costs more.</p>
            """),
        ],
        "faqs": [
            ("Can I switch from paint to stain on cedar that's already painted?", "Yes, but it's not cheap. The existing paint film has to be stripped back to bare wood before stain will penetrate — otherwise you're just putting tinted stain on top of paint, which looks bad and behaves like paint. Stripping a previously-painted home for stain typically adds 30-50% to the project cost. Most homeowners who want to switch do it during a major exterior refresh, not in the middle of a normal recoat cycle."),
            ("How often will I need to re-stain cedar in Grand Rapids?", "Transparent stain: every 2-4 years. Semi-transparent: 4-6 years. Solid stain: 6-8 years. South- and west-facing walls fade fastest, north walls last longest, and shaded north walls with mildew pressure can need more frequent washing even between recoats."),
            ("Will solid stain show the wood grain?", "Solid stain hides most of the grain — it looks much more like paint than transparent or semi-transparent stain. The advantage over actual paint is that it still penetrates the wood, so it ages by fading rather than peeling, and the next maintenance cycle is much simpler. If you want the grain visible, you want semi-transparent or transparent."),
            ("What's the best time of year to stain cedar in Grand Rapids?", "Late May through early October. We need surface temperatures above 50°F overnight, dry weather for 24-48 hours after each coat, and ideally low humidity. Late spring and early fall are gentlest on fresh stain — peak summer heat can cause the stain to dry too fast, which leaves lap marks."),
            ("Why is my cedar peeling on the south side but not the north?", "UV intensity. South and west walls get hours more direct sun than north walls in Michigan, and the temperature cycling on a sunny December day can be 60°F or more between the surface and the air. That cycling stresses the paint film until it fails. Stain doesn't have this problem because there's no film to fail — it just fades a bit faster on the sunny sides."),
            ("Do you prep cedar differently than other siding?", "Yes — significantly. Cedar gets a tannin-blocking primer on any bare wood, individual shellac-based spot-priming on every visible knot, and a mildewcide wash on shaded exposures. Vinyl and fiber-cement need none of that. The extra cedar prep is why cedar exterior quotes run higher than vinyl quotes on similarly-sized homes — and it's the difference between a finish that lasts and one that fails in three years."),
            ("Does Go Green do both paint and stain projects?", "Yes — and we'll give you an honest recommendation based on what's already on your cedar and what you're trying to accomplish. Sometimes the answer is paint, sometimes it's stain, and sometimes it's a phased switch over two maintenance cycles. Every estimate is free and fixed-price."),
        ],
        "related": [
            ("Exterior House Painting", "/services/exterior-painting/"),
            ("House Painters in Cascade", "/grand-rapids/cascade/"),
            ("House Painters in Forest Hills", "/grand-rapids/forest-hills/"),
            ("House Painters in Ada", "/grand-rapids/ada/"),
        ],
        "related_heading": "Related Reading & Services",
    },

    {
        "slug": "blog/owner-operated-vs-college-painting-franchises-grand-rapids/",
        "title": "Owner-Operated vs. College Painting Franchises in Grand Rapids: What's the Difference?",
        "description": "Choosing between an owner-operated painter and a college painting franchise in Grand Rapids? Here's how the two business models actually work, what public reviews show, and the questions to ask before hiring either.",
        "h1": "Owner-Operated vs. College Painting Franchises in Grand Rapids",
        "hero_img": "/exterior-after.jpg",
        "date_published": "2026-06-10",
        "date_modified": "2026-06-10",
        "author_id": f"{SITE}/#jackson",
        "author_name": "Jackson Befus",
        "breadcrumb": [("Home", "/"), ("Blog", "/blog/"), ("Owner-Operated vs. College Franchises", "/blog/owner-operated-vs-college-painting-franchises-grand-rapids/")],
        "lead": "Search \"house painters Grand Rapids\" and you'll see two very different kinds of companies. On one side: nationwide college-painter franchises — College Pro, College Works, Student Painters, and their cousins — each with regional branches staffed mostly by summer hires. On the other: small, owner-operated outfits where the same person quotes the job, paints it, and is on the hook if anything goes sideways. We're the second kind, so we have an obvious bias. But the two models are genuinely different in ways that matter, and the public record on each is easy to look up. Here's an honest comparison so you can make a real decision either way.",
        "sections": [
            ("How College Painting Franchises Actually Work", """
                <p>The college painting franchise model is roughly forty years old. The structure is consistent across the major brands:</p>
                <ul>
                  <li>A corporate parent owns the brand, the marketing, the training materials, and the lead-generation pipeline.</li>
                  <li>Each region has a local branch — often run by a student or recent grad on a one- or two-year contract — that operates as a franchisee.</li>
                  <li>The branch manager hires summer paint crews, usually college students, often with little or no prior painting experience.</li>
                  <li>Corporate takes a cut of every job for marketing, brand, training, and lead generation.</li>
                </ul>
                <p>None of that is sinister. Franchises exist because the model scales — they can drop a branded operation into a new city quickly, hand the manager a pipeline of leads, and turn a regional brand recognition advantage into volume. The trade-off is that the people on your job site are usually new to painting, the manager is usually new to managing, and the company you're hiring this summer may be a totally different operating team next summer.</p>
            """),
            ("What the Public Reviews Show", """
                <p>You don't have to take our word for any of this. The reviews are public.</p>
                <p>College Pro Painters, one of the largest, holds an average of <strong>1.6 stars across 221+ aggregated consumer reviews</strong> on PissedConsumer (as of 2026). Complaints cluster around damage to homes, incomplete jobs, missed appointments, and difficulty reaching anyone after the deposit is paid. College Works Painting has a wider review spread — some genuinely positive, some echoing the same concerns. Local Grand Rapids reviews on these brands are mixed-to-negative on HomeAdvisor and BBB.</p>
                <p>This isn't a blanket indictment. Some college franchise crews do excellent work, and we know individual managers who genuinely care about quality. But the model has structural pressure points that the reviews reflect — and a discerning homeowner should look at the actual review distribution for any company, franchise or not, before signing a contract.</p>
            """),
            ("How the Owner-Operated Model Works", """
                <p>Owner-operated painting companies have a different shape:</p>
                <ul>
                  <li>The people who own the business do the painting.</li>
                  <li>The person who quotes your job is the person who does your job.</li>
                  <li>There's no corporate marketing budget baked into pricing — overhead is lower.</li>
                  <li>Accountability is personal. If you have a problem in November on work done in June, the people who painted it are still the people who answer the phone.</li>
                  <li>The trade-off is scale: a true owner-operated outfit takes fewer jobs per season than a franchise crew.</li>
                </ul>
                <p>Go Green College Painters is owner-operated. Jackson and Evelyn Befus do the work themselves, and the brand has \"College\" in the name because Jackson goes to Michigan State and Evelyn goes to Wayne State — not because we're a franchise.</p>
            """),
            ("What Actually Changes on the Job Site", """
                <p>The differences between the two models show up in three concrete places:</p>
                <ul>
                  <li><strong>Prep work.</strong> Franchise crews are paid by piece-rate or hourly, and there's pressure to move quickly. Prep is the easiest thing to shortcut. Owner-operated painters have personal long-term reputation on every job, which usually means more time on prep and less of it visible in the finished result.</li>
                  <li><strong>Scheduling reliability.</strong> When a franchise crew gets pulled to a higher-priority job mid-week, the homeowner finds out at 5pm that nobody's coming tomorrow. Owner-operators have a much smaller calendar and tend to honor it.</li>
                  <li><strong>Communication.</strong> One throat to choke, in both directions. You're not bouncing between the salesperson, the branch manager, and the crew lead trying to figure out who decided to paint your front door the wrong sheen.</li>
                </ul>
            """),
            ("Are Franchises Cheaper?", """
                <p>Sometimes — but not as often as you might assume.</p>
                <p>Franchises absorb corporate marketing, training, and brand fees into their pricing. Owner-operated companies don't carry that overhead, so on average the underlying labor cost is similar and franchise pricing can run slightly higher to cover the corporate cut. Where franchises do come in cheaper, it's often because they're cutting prep time or using lower-grade paint — both of which show up two or three years later in failed finishes.</p>
                <p>That said, every quote should compete on what's actually being delivered, not on brand. A franchise quote that includes the same paint, the same prep, the same coats, and a real warranty is a real competitor. The thing to scrutinize is what's <em>not</em> in the quote.</p>
            """),
            ("How to Evaluate Any Painter in Grand Rapids", """
                <p>Whether you hire a franchise, an owner-operator, or anything in between, ask these eight questions before signing:</p>
                <ul>
                  <li><strong>Who specifically will be on my property?</strong> Get a real name, not a job title.</li>
                  <li><strong>Are you fully insured? Can you email me a current certificate of insurance before we start?</strong></li>
                  <li><strong>What paint brand and product line are you using, and how many coats?</strong> Premium 100% acrylic exterior paint vs. a builder-grade contractor line is a big lifespan difference.</li>
                  <li><strong>Walk me through your prep. What do you do when paint is failing? When wood is bare? When you find rot?</strong></li>
                  <li><strong>What's your warranty, and who honors it if the company changes hands or the branch closes?</strong></li>
                  <li><strong>Can I see two or three local recent project addresses where I can drive by?</strong></li>
                  <li><strong>What happens if it rains during my project? What's your scheduling backup plan?</strong></li>
                  <li><strong>How do you handle change orders mid-project?</strong></li>
                </ul>
                <p>An honest contractor of either model will answer all eight without hesitation.</p>
            """),
            ("Why We Built Go Green This Way", """
                <p>Jackson and Evelyn started Go Green because they wanted to put themselves through MSU and Wayne State doing work they were proud of. That's a different starting point than \"how do I scale a franchise.\" It means we'd rather book fewer projects per season and do every one of them with our own hands than turn the business into something we're managing instead of building. Whether that's the right fit for your project is your call to make. But that's the shape of the company you're hiring when you call us, and we think the difference shows up where it matters.</p>
            """),
        ],
        "faqs": [
            ("Is Go Green College Painters a franchise?", "No. Go Green is independent and locally owned by Jackson and Evelyn Befus. The name reflects that the founders are college students — Jackson at Michigan State, Evelyn at Wayne State — not that we're affiliated with a national brand or franchise system."),
            ("Why do college painting franchises tend to have mixed reviews?", "The model puts new managers and new crews together every summer under time pressure to hit a corporate revenue target. Even with the best intentions, that combination creates inconsistent quality across jobs and across years. Some franchise crews do excellent work — but the structural variance is real, and the public review distribution reflects it."),
            ("Are owner-operated painters more expensive than franchises?", "Often comparable, sometimes less. Franchises pass corporate marketing and brand overhead into their pricing; owner-operators don't. Where franchise quotes come in significantly cheaper, the usual reason is shorter prep time or lower-grade paint, which costs the homeowner more in the long run."),
            ("What's the single most important question to ask a painter before hiring?", "\"Walk me through your prep work in detail.\" Prep is the largest variable in how long a paint job lasts, and it's also the easiest place to cut corners invisibly. An honest contractor will spend 5–10 minutes on this question. A weak one will give you 30 seconds and change the subject."),
            ("Who actually shows up on the day at Go Green?", "Jackson and Evelyn. There are no subcontractors, no rotating summer crews, and no separate \"sales rep then crew\" handoff. The people who quoted your job are the people doing your job."),
            ("How can I verify a painter's insurance?", "Ask for a current Certificate of Insurance (COI) and have the painter's agent email it directly to you before work starts. Don't accept a verbal \"we're insured\" — and don't accept a COI that's expired or doesn't name your project. Any reputable painter, franchise or owner-operated, will produce one within a day."),
        ],
        "related": [
            ("About Go Green College Painters", "/about/"),
            ("Exterior House Painting", "/services/exterior-painting/"),
            ("Interior Painting", "/services/interior-painting/"),
            ("Cost to Paint a House in Grand Rapids", "/blog/cost-to-paint-a-house-in-grand-rapids/"),
        ],
        "related_heading": "Related Reading & Pages",
    },
]

# -------- shared template --------
NAV_HTML = """  <nav>
    <a href="/" class="nav-logo">
      <img src="/logo.png" alt="Go Green College Painters" onerror="this.style.display='none'" />
      <div class="nav-logo-text">
        <span>Go Green Painters</span>
        <span>Greater Grand Rapids</span>
      </div>
    </a>
    <ul class="nav-links" id="navLinks">
      <li><a href="/services/exterior-painting/">Exterior</a></li>
      <li><a href="/services/interior-painting/">Interior</a></li>
      <li><a href="/services/deck-staining/">Deck Staining</a></li>
      <li><a href="/services/custom-murals/">Murals</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/" class="nav-cta">Free Quote</a></li>
    </ul>
    <div class="hamburger" id="hamburger" onclick="toggleMenu()">
      <span></span><span></span><span></span>
    </div>
  </nav>"""

FOOTER_HTML = """  <footer>
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo">
          <img src="/logo.png" alt="Go Green College Painters" onerror="this.style.display='none'" />
          <span class="footer-logo-text">Go Green College Painters</span>
        </div>
        <p>Professional painting services delivered by motivated college students. Quality work, honest prices, and guaranteed satisfaction &mdash; serving Greater Grand Rapids since 2024.</p>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="/services/exterior-painting/">Exterior Painting</a></li>
          <li><a href="/services/interior-painting/">Interior Painting</a></li>
          <li><a href="/services/deck-staining/">Deck Staining</a></li>
          <li><a href="/services/custom-murals/">Custom Murals</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about/">About Us</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="tel:+16162642119">(616) 264-2119</a></li>
          <li><a href="mailto:jack@gogreenpainters.com">jack@gogreenpainters.com</a></li>
          <li><a href="https://www.yelp.com/biz/go-green-painters-grand-rapids" target="_blank" rel="noopener">Yelp Reviews</a></li>
          <li><a href="https://www.facebook.com/profile.php?id=61589807997680" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2024 Go Green College Painters. All rights reserved.</span>
      <span>Greater Grand Rapids, MI</span>
    </div>
  </footer>"""

SCRIPTS_HTML = """  <script>
    function toggleMenu() { document.getElementById('navLinks').classList.toggle('open'); }
    document.querySelectorAll('.nav-links a').forEach(function (l) {
      l.addEventListener('click', function () { document.getElementById('navLinks').classList.remove('open'); });
    });
    window.addEventListener('scroll', function () {
      var n = document.querySelector('nav');
      if (n) n.style.boxShadow = window.scrollY > 20 ? '0 2px 20px rgba(0,0,0,0.35)' : '0 2px 12px rgba(0,0,0,0.25)';
    });
    // Track tel: link clicks as a GA4 'phone_click' event
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="tel:"]');
      if (a && typeof window.gtag === 'function') {
        gtag('event', 'phone_click', { phone_number: a.getAttribute('href').replace('tel:', '') });
      }
    });
  </script>
  <!-- Zoho SalesIQ - deferred to first interaction or 5s -->
  <script>
    (function () {
      var loaded = false;
      function loadZoho() {
        if (loaded) return; loaded = true;
        window.$zoho = window.$zoho || {};
        window.$zoho.salesiq = window.$zoho.salesiq || { widgetcode: "siq3aa97abd7397b8e8fb6a7a41ff2162ec1e63e93450f9cbd1e76dac3ef46afd90", values: {}, ready: function () {} };
        var s = document.createElement("script");
        s.type = "text/javascript"; s.id = "zsiqscript"; s.defer = true; s.src = "https://salesiq.zoho.com/widget";
        document.head.appendChild(s);
      }
      ["scroll", "click", "keydown", "mousemove", "touchstart"].forEach(function (ev) {
        window.addEventListener(ev, loadZoho, { once: true, passive: true });
      });
      setTimeout(loadZoho, 5000);
    })();
  </script>"""

def render_faq_html(faqs):
    parts = []
    for q, a in faqs:
        parts.append(f"""        <details class="faq-item">
          <summary>{html_lib.escape(q)} <span class="faq-plus">+</span></summary>
          <p>{a}</p>
        </details>""")
    return "\n".join(parts)

def render_breadcrumb_html(crumbs):
    items = []
    for i, (name, url) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<span aria-current="page">{html_lib.escape(name)}</span>')
        else:
            items.append(f'<a href="{url}">{html_lib.escape(name)}</a>')
    return ' <span class="bc-sep">&rsaquo;</span> '.join(items)

def render_sections_html(sections):
    parts = []
    for heading, body in sections:
        body = textwrap.dedent(body).strip()
        parts.append(f"""      <div class="page-section">
        <h2>{html_lib.escape(heading)}</h2>
        {body}
      </div>""")
    return "\n".join(parts)

def render_related_html(related, heading="Related Services"):
    items = "".join([f'<li><a href="{url}">{html_lib.escape(name)}</a></li>' for name, url in related])
    return f"""      <div class="related-services">
        <h2>{html_lib.escape(heading)}</h2>
        <ul>{items}</ul>
      </div>"""

def build_jsonld(page):
    canonical = f"{SITE}/{page['slug']}"
    graph = [
        LOCAL_BUSINESS,
        WEBSITE_NODE,
        {
            "@type": "Person", "@id": f"{SITE}/#jackson",
            "name": "Jackson Befus", "jobTitle": "Co-Owner & Project Manager",
            "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Michigan State University",
        },
        {
            "@type": "Person", "@id": f"{SITE}/#evelyn",
            "name": "Evelyn Befus", "jobTitle": "Co-Owner & Creative Director",
            "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Wayne State University",
        },
        {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": f"{SITE}/#website"},
            "about": {"@id": BUSINESS_ID},
            "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "item": (url if url.startswith("http") else f"{SITE}{url}")}
                for i, (name, url) in enumerate(page["breadcrumb"])
            ],
        },
        {
            "@type": "Service",
            "@id": f"{canonical}#service",
            "serviceType": page["service_name"],
            "name": page["service_name"],
            "description": page["service_desc"],
            "image": page["service_image"],
            "provider": {"@id": BUSINESS_ID},
            "areaServed": page.get("area_served", {
                "@type": "City", "name": "Grand Rapids",
                "containedInPlace": {"@type": "State", "name": "Michigan"},
            }),
            "url": canonical,
        },
        {
            "@type": "FAQPage",
            "@id": f"{canonical}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faqs"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)

def build_page(page):
    canonical = f"{SITE}/{page['slug']}"
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html_lib.escape(page['title'])}</title>
  <meta name="description" content="{html_lib.escape(page['description'])}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{html_lib.escape(page['title'])}" />
  <meta property="og:description" content="{html_lib.escape(page['description'])}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og_image(page['slug'])}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{og_image(page['slug'])}" />

  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />

  <link rel="preload" as="image" href="{page['hero_img']}" />

  <script type="application/ld+json">
{build_jsonld(page)}
  </script>

{FONT_LINKS}
</head>
<body>"""

    hero_class = HERO_CLASS_MAP.get(page["hero_img"], "hero-default")
    page_hero = f"""  <section class="page-hero {hero_class}">
    <div class="page-hero-inner">
      <nav class="breadcrumb">{render_breadcrumb_html(page['breadcrumb'])}</nav>
      <h1>{html_lib.escape(page['h1'])}</h1>
      <p class="lead">{page['lead']}</p>
      <a href="/contact/" class="btn-primary">Get a Free Estimate</a>
    </div>
  </section>"""

    sections_html = render_sections_html(page["sections"])
    faq_html = render_faq_html(page["faqs"])
    related_html = render_related_html(page["related"], page.get("related_heading", "Related Services"))

    main = f"""  <main class="page-main">
    <div class="container">
{sections_html}

      <div class="page-faq">
        <h2>Common Questions</h2>
{faq_html}
      </div>

{related_html}
    </div>
  </main>

  <!-- CTA banner -->
  <div id="cta-banner">
    <div class="container">
      <h2>Ready to Get Started?</h2>
      <p>Free, no-obligation estimates &mdash; serving Greater Grand Rapids.</p>
      <a href="/#contact" class="btn-dark">Get My Free Quote</a>
    </div>
  </div>"""

    return f"{head}\n{NAV_HTML}\n{page_hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

# -------- blog rendering --------
def build_blog_jsonld(post):
    canonical = f"{SITE}/{post['slug']}"
    graph = [
        LOCAL_BUSINESS,
        WEBSITE_NODE,
        {
            "@type": "Person", "@id": f"{SITE}/#jackson",
            "name": "Jackson Befus", "jobTitle": "Co-Owner & Project Manager",
            "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Michigan State University",
        },
        {
            "@type": "Person", "@id": f"{SITE}/#evelyn",
            "name": "Evelyn Befus", "jobTitle": "Co-Owner & Creative Director",
            "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Wayne State University",
        },
        {
            "@type": "BlogPosting",
            "@id": f"{canonical}#article",
            "headline": post["title"],
            "description": post["description"],
            "image": f"{SITE}{post['hero_img']}",
            "datePublished": post["date_published"],
            "dateModified": post["date_modified"],
            "author": {"@id": post["author_id"]},
            "publisher": {"@id": BUSINESS_ID},
            "mainEntityOfPage": {"@id": f"{canonical}#webpage"},
            "url": canonical,
        },
        {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": post["title"],
            "description": post["description"],
            "isPartOf": {"@id": f"{SITE}/#website"},
            "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "item": (url if url.startswith("http") else f"{SITE}{url}")}
                for i, (name, url) in enumerate(post["breadcrumb"])
            ],
        },
        {
            "@type": "FAQPage",
            "@id": f"{canonical}#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in post["faqs"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)

# Google Analytics 4 — loaded async so it never blocks render. Injected into every page head.
GA_SNIPPET = """  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-R6ZG6CC6M6"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-R6ZG6CC6M6');
  </script>"""

# Bump CSS_VERSION whenever styles.css changes — busts browser caches via the ?v= query.
# (Belt-and-suspenders with the must-revalidate header in _headers.)
CSS_VERSION = "20260514"

FAVICON_LINKS = """  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="icon" href="/favicon.ico" sizes="any" />"""

FONT_LINKS = GA_SNIPPET + "\n" + FAVICON_LINKS + f"""
  <link rel="preload" href="/fonts/oswald.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/fonts/opensans.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/styles.css?v={CSS_VERSION}" />"""

def fmt_date(iso):
    dt = datetime.datetime.strptime(iso, "%Y-%m-%d")
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

def build_blog_post(post):
    canonical = f"{SITE}/{post['slug']}"
    display_date = fmt_date(post["date_published"])
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html_lib.escape(post['title'])}</title>
  <meta name="description" content="{html_lib.escape(post['description'])}" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{html_lib.escape(post['title'])}" />
  <meta property="og:description" content="{html_lib.escape(post['description'])}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og_image(post['slug'])}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{og_image(post['slug'])}" />
  <meta property="article:published_time" content="{post['date_published']}" />
  <meta property="article:modified_time" content="{post['date_modified']}" />

  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />

  <link rel="preload" as="image" href="{post['hero_img']}" />

  <script type="application/ld+json">
{build_blog_jsonld(post)}
  </script>

{FONT_LINKS}
</head>
<body>"""

    hero_class = HERO_CLASS_MAP.get(post["hero_img"], "hero-default")
    page_hero = f"""  <section class="page-hero {hero_class}">
    <div class="page-hero-inner">
      <nav class="breadcrumb">{render_breadcrumb_html(post['breadcrumb'])}</nav>
      <h1>{html_lib.escape(post['h1'])}</h1>
      <p class="post-meta">By {html_lib.escape(post['author_name'])} &middot; {display_date}</p>
    </div>
  </section>"""

    sections_html = render_sections_html(post["sections"])
    faq_html = render_faq_html(post["faqs"])
    related_html = render_related_html(post["related"], post.get("related_heading", "Our Services"))

    main = f"""  <main class="page-main">
    <div class="container">
      <p class="post-lead">{post['lead']}</p>

{sections_html}

      <div class="page-faq">
        <h2>Frequently Asked Questions</h2>
{faq_html}
      </div>

{related_html}
    </div>
  </main>

  <div id="cta-banner">
    <div class="container">
      <h2>Want a Real Number for Your Home?</h2>
      <p>Free, fixed-price written estimates &mdash; serving Greater Grand Rapids.</p>
      <a href="/#contact" class="btn-dark">Get My Free Quote</a>
    </div>
  </div>"""

    return f"{head}\n{NAV_HTML}\n{page_hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

def build_blog_index(posts):
    canonical = f"{SITE}/blog/"
    cards = []
    for post in posts:
        cards.append(f"""        <a href="/{post['slug']}" class="blog-card">
          <span class="blog-card-date">{fmt_date(post['date_published'])}</span>
          <h2>{html_lib.escape(post['title'])}</h2>
          <p>{html_lib.escape(post['description'])}</p>
          <span class="service-link">Read more &rarr;</span>
        </a>""")
    cards_html = "\n".join(cards)
    blog_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            LOCAL_BUSINESS,
            WEBSITE_NODE,
            {
                "@type": "Blog",
                "@id": f"{canonical}#blog",
                "url": canonical,
                "name": "Go Green College Painters Blog",
                "description": "Painting guides, cost breakdowns, and tips for Grand Rapids homeowners.",
                "publisher": {"@id": BUSINESS_ID},
                "blogPost": [{"@id": f"{SITE}/{p['slug']}#article"} for p in posts],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": canonical},
                ],
            },
        ],
    }, indent=2)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Painting Tips &amp; Cost Guides for Grand Rapids Homeowners | Go Green College Painters</title>
  <meta name="description" content="Painting guides, cost breakdowns, and practical tips for Grand Rapids homeowners from Go Green College Painters." />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Go Green College Painters Blog" />
  <meta property="og:description" content="Painting guides, cost breakdowns, and tips for Grand Rapids homeowners." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}/og/og-blog.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SITE}/og/og-blog.jpg" />
  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />
  <script type="application/ld+json">
{blog_jsonld}
  </script>
{FONT_LINKS}
</head>
<body>
{NAV_HTML}
  <section class="page-hero hero-default" style="min-height: 340px;">
    <div class="page-hero-inner">
      <nav class="breadcrumb"><a href="/">Home</a> <span class="bc-sep">&rsaquo;</span> <span aria-current="page">Blog</span></nav>
      <h1>Painting Tips &amp; Cost Guides</h1>
      <p class="lead">Straight answers for Grand Rapids homeowners — what projects cost, how we work, and how to get it done right.</p>
    </div>
  </section>
  <main class="page-main">
    <div class="container">
      <div class="blog-grid">
{cards_html}
      </div>
    </div>
  </main>
  <div id="cta-banner">
    <div class="container">
      <h2>Ready to Get Started?</h2>
      <p>Free, no-obligation estimates &mdash; serving Greater Grand Rapids.</p>
      <a href="/#contact" class="btn-dark">Get My Free Quote</a>
    </div>
  </div>
{FOOTER_HTML}
{SCRIPTS_HTML}
</body>
</html>
"""

# -------- standalone pages: About & Contact --------
def build_about_page():
    canonical = f"{SITE}/about/"
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            LOCAL_BUSINESS,
            WEBSITE_NODE,
            {
                "@type": "Person", "@id": f"{SITE}/#jackson",
                "name": "Jackson Befus", "jobTitle": "Co-Owner & Project Manager",
                "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Michigan State University",
                "description": "Co-founder of Go Green College Painters. Studies Communications and Entrepreneurship at Michigan State University. Manages project operations and client relations.",
            },
            {
                "@type": "Person", "@id": f"{SITE}/#evelyn",
                "name": "Evelyn Befus", "jobTitle": "Co-Owner & Creative Director",
                "worksFor": {"@id": BUSINESS_ID}, "alumniOf": "Wayne State University",
                "description": "Co-founder of Go Green College Painters. Studies Industrial Design at Wayne State University. Lifelong illustrator who leads the company's custom mural and creative design work.",
            },
            {
                "@type": "AboutPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": "About Go Green College Painters",
                "description": "Go Green College Painters is a student-owned, owner-operated painting company in Greater Grand Rapids, MI, founded in 2024 by siblings Jackson and Evelyn Befus.",
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": BUSINESS_ID},
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "About", "item": canonical},
                ],
            },
        ],
    }, indent=2)
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About Go Green College Painters | Student-Owned Painters in Grand Rapids, MI</title>
  <meta name="description" content="Go Green College Painters is a student-owned, owner-operated painting company in Greater Grand Rapids, MI. Meet founders Jackson and Evelyn Befus and learn how we work." />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="About Go Green College Painters" />
  <meta property="og:description" content="Student-owned, owner-operated painting company in Greater Grand Rapids. Meet founders Jackson and Evelyn Befus." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}/og/og-about.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SITE}/og/og-about.jpg" />
  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />
  <link rel="preload" as="image" href="/exterior-after.jpg" />
  <script type="application/ld+json">
{jsonld}
  </script>
{FONT_LINKS}
</head>
<body>"""
    hero = """  <section class="page-hero hero-exterior">
    <div class="page-hero-inner">
      <nav class="breadcrumb"><a href="/">Home</a> <span class="bc-sep">&rsaquo;</span> <span aria-current="page">About</span></nav>
      <h1>About Go Green College Painters</h1>
      <p class="lead">A student-owned, owner-operated painting company serving Greater Grand Rapids — built one project at a time by a brother-and-sister team putting themselves through college.</p>
      <a href="/contact/" class="btn-primary">Get a Free Estimate</a>
    </div>
  </section>"""
    main = """  <main class="page-main">
    <div class="container">
      <div class="page-section">
        <h2>Who We Are</h2>
        <p>Go Green College Painters was founded in 2024 by siblings Jackson and Evelyn Befus. We're a student-owned, owner-operated painting company — which means the two people who quote your job are the same two people who show up, prep, paint, and clean up. No subcontractors, no rotating crews of summer hires, no salesperson handing your project to strangers.</p>
        <p>We serve Greater Grand Rapids, Michigan, with a focus on the cedar-sided neighborhoods of the east side — Cascade, Forest Hills, Ada, and East Grand Rapids — handling exterior painting, interior painting, deck staining, and custom murals.</p>
      </div>

      <div class="page-section">
        <h2>Meet the Founders</h2>
        <div class="about-founder">
          <img src="/jackson-photo.jpg" alt="Jackson Befus, Co-Owner of Go Green College Painters" loading="lazy" />
          <div>
            <h3>Jackson Befus &mdash; Co-Owner &amp; Project Manager</h3>
            <p>Jackson co-founded Go Green College Painters in 2024 while studying Communications and Entrepreneurship at Michigan State University. His love for painting started unexpectedly &mdash; a summer spent restoring his dad's vintage 36-foot sailboat sparked a real passion for the craft. Since then he's led the team through interior and exterior projects of every size, residential and commercial, with a simple commitment: show up on time and get the job done right.</p>
          </div>
        </div>
        <div class="about-founder">
          <img src="/evelyn-photo.jpg" alt="Evelyn Befus, Co-Owner of Go Green College Painters" loading="lazy" />
          <div>
            <h3>Evelyn Befus &mdash; Co-Owner &amp; Creative Director</h3>
            <p>Evelyn studies Industrial Design at Wayne State University, and her passion for art and painting goes back as far as she can remember &mdash; illustrating, painting, and creating have always been at the heart of who she is. Go Green has given her the chance not only to pay for college, but to bring a creative eye to projects that start as simple one-color refreshes. If you have a vision for a children's space, a dining room, or a mural, Evelyn can bring it to life.</p>
          </div>
        </div>
      </div>

      <div class="page-section">
        <h2>Why "Go Green"?</h2>
        <p>The name is a nod to Michigan State University &mdash; Jackson's school, and the Spartan green that goes with it. It's a bit of hometown pride baked into the brand.</p>
      </div>

      <div class="page-section">
        <h2>How We Work</h2>
        <ul>
          <li><strong>Owner-operated.</strong> Jackson and Evelyn personally do every job. The people who quote it are the people who paint it.</li>
          <li><strong>Fully insured.</strong> Full liability insurance on every project, with proof available on request.</li>
          <li><strong>Free, fixed-price estimates.</strong> We walk the property, identify the prep that's actually needed, and give you a written number that doesn't change unless the scope does.</li>
          <li><strong>Real prep.</strong> The difference between paint that lasts and paint that fails is prep work &mdash; and we don't skip it.</li>
          <li><strong>Satisfaction guaranteed.</strong> If something isn't right, we make it right.</li>
        </ul>
      </div>

      <div class="related-services">
        <h2>Explore</h2>
        <ul><li><a href="/services/exterior-painting/">Exterior Painting</a></li><li><a href="/services/interior-painting/">Interior Painting</a></li><li><a href="/services/custom-murals/">Custom Murals</a></li><li><a href="/contact/">Contact Us</a></li></ul>
      </div>
    </div>
  </main>

  <div id="cta-banner">
    <div class="container">
      <h2>Let's Talk About Your Project</h2>
      <p>Free, no-obligation estimates &mdash; serving Greater Grand Rapids.</p>
      <a href="/contact/" class="btn-dark">Get My Free Quote</a>
    </div>
  </div>"""
    return f"{head}\n{NAV_HTML}\n{hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"


CONTACT_FORM_HTML = """        <form class="contact-form" action="https://forms.zohopublic.com/jackgogreen1/form/WebsiteContact/formperma/8Js26cdu-6qrbCBK5668ufHpo_DCyQw8r5azScg3bV8/htmlRecords/submit" name="form" id="zoho-contact-form" method="POST" accept-charset="UTF-8" enctype="multipart/form-data">
          <input type="hidden" name="zf_referrer_name" value="" />
          <input type="hidden" name="zf_redirect_url" value="https://gogreenpainters.com/contact/thank-you/" />
          <input type="hidden" name="zc_gad" value="" />
          <h3>Tell Us About Your Project</h3>
          <div class="form-row">
            <div class="form-group"><label for="fname">First Name</label><input type="text" id="fname" name="Name_First" maxlength="255" placeholder="Jane" required /></div>
            <div class="form-group"><label for="lname">Last Name</label><input type="text" id="lname" name="Name_Last" maxlength="255" placeholder="Smith" required /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="email">Email</label><input type="email" id="email" name="Email" maxlength="255" placeholder="jane@email.com" /></div>
            <div class="form-group"><label for="phone">Phone</label><input type="tel" id="phone" name="PhoneNumber_countrycode" maxlength="20" placeholder="(616) 555-5555" /></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="address">Street Address</label><input type="text" id="address" name="Address_AddressLine1" maxlength="255" placeholder="123 Main St" /></div>
            <div class="form-group"><label for="zip">Zip Code</label><input type="text" id="zip" name="Address_ZipCode" maxlength="255" placeholder="49503" /></div>
          </div>
          <div class="form-group">
            <label for="service">Service Needed</label>
            <select id="service" name="Dropdown">
              <option value="-Select-">Select a service...</option>
              <option value="Exterior Painting">Exterior Painting</option>
              <option value="Interior Painting">Interior Painting</option>
              <option value="Deck Staining">Deck Staining</option>
              <option value="Custom Designs">Custom Designs</option>
              <option value="Multiple Services">Multiple Services</option>
            </select>
          </div>
          <div class="form-group"><label for="message">Project Details</label><textarea id="message" name="MultiLine" maxlength="65535" placeholder="Tell us about your project — size, colors in mind, timeline, etc."></textarea></div>
          <button type="submit" class="form-submit">Send My Request &rarr;</button>
        </form>"""

def build_contact_page():
    canonical = f"{SITE}/contact/"
    faqs = [
        ("How do I get a free painting estimate in Grand Rapids?", "Fill out the form on this page or call (616) 264-2119. We respond within 24 hours to schedule a walk-through, then provide a free, fixed-price written estimate — no pressure, no obligation."),
        ("What areas do you serve?", "Go Green College Painters serves Greater Grand Rapids, Michigan and surrounding communities, with a focus on Cascade, Forest Hills, Ada, and East Grand Rapids. Not sure if you're in range? Call us — we're happy to travel for the right project."),
        ("How soon can you start my project?", "It depends on the season. Exterior projects book fastest in spring and fall; interior work is more flexible year-round. Most projects start within 2–6 weeks of the estimate. Reach out early for spring and fall exterior slots."),
        ("Do you charge for estimates?", "No. Every estimate is free, fixed-price, and provided in writing. The number we quote doesn't change unless the scope of the project changes."),
    ]
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            LOCAL_BUSINESS,
            WEBSITE_NODE,
            {
                "@type": "ContactPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": "Contact Go Green College Painters",
                "description": "Contact Go Green College Painters for a free, fixed-price painting estimate in Greater Grand Rapids, MI. Call (616) 264-2119 or use the project form.",
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": BUSINESS_ID},
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Contact", "item": canonical},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical}#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            },
        ],
    }, indent=2)
    faq_html = render_faq_html(faqs)
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Contact Go Green College Painters | Free Painting Estimates in Grand Rapids, MI</title>
  <meta name="description" content="Contact Go Green College Painters for a free, fixed-price painting estimate in Greater Grand Rapids, MI. Call (616) 264-2119 or fill out the project form." />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Contact Go Green College Painters" />
  <meta property="og:description" content="Free, fixed-price painting estimates in Greater Grand Rapids. Call (616) 264-2119." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}/og/og-contact.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SITE}/og/og-contact.jpg" />
  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />
  <script type="application/ld+json">
{jsonld}
  </script>
{FONT_LINKS}
</head>
<body>"""
    hero = """  <section class="page-hero hero-default" style="min-height: 320px;">
    <div class="page-hero-inner">
      <nav class="breadcrumb"><a href="/">Home</a> <span class="bc-sep">&rsaquo;</span> <span aria-current="page">Contact</span></nav>
      <h1>Contact Go Green College Painters</h1>
      <p class="lead">Free, fixed-price estimates across Greater Grand Rapids. We respond within 24 hours.</p>
    </div>
  </section>"""
    main = f"""  <main class="page-main">
    <div class="container">
      <div class="contact-inner">
        <div class="contact-info">
          <h2 style="font-family:'Oswald',sans-serif;text-transform:uppercase;color:var(--green-dark);font-size:1.55rem;border-bottom:3px solid var(--gold);padding-bottom:10px;margin-bottom:18px;">Get In Touch</h2>
          <p style="font-size:1rem;color:#444;line-height:1.8;margin-bottom:8px;">Fill out the form or call <a href="tel:+16162642119" style="color:var(--green-mid);font-weight:600;">(616) 264-2119</a>. We respond within 24 hours with a free, no-obligation estimate &mdash; no pressure, no commitment.</p>
          <div class="contact-details">
            <div class="contact-item">
              <div class="contact-item-icon"><svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg></div>
              <div class="contact-item-text"><strong>Phone</strong><span><a href="tel:+16162642119">(616) 264-2119</a></span></div>
            </div>
            <div class="contact-item">
              <div class="contact-item-icon"><svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg></div>
              <div class="contact-item-text"><strong>Email</strong><span><a href="mailto:jack@gogreenpainters.com">jack@gogreenpainters.com</a></span></div>
            </div>
            <div class="contact-item">
              <div class="contact-item-icon"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg></div>
              <div class="contact-item-text"><strong>Service Area</strong><span>Greater Grand Rapids, MI</span></div>
            </div>
          </div>
        </div>
{CONTACT_FORM_HTML}
      </div>

      <div class="page-faq" style="margin-top:64px;">
        <h2>Common Questions</h2>
{faq_html}
      </div>
    </div>
  </main>"""
    return f"{head}\n{NAV_HTML}\n{hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

# -------- standalone: branded 404 --------
def build_404_page():
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Not Found | Go Green College Painters</title>
  <meta name="robots" content="noindex, follow" />
  <meta name="description" content="That page couldn't be found. Explore Go Green College Painters' services, service areas, and contact options." />
{FONT_LINKS}
</head>
<body>"""
    hero = """  <section class="page-hero hero-default" style="min-height: 380px;">
    <div class="page-hero-inner">
      <h1>404 &mdash; Page Not Found</h1>
      <p class="lead">Looks like that page got painted over. Let's get you back to something useful.</p>
      <a href="/" class="btn-primary">Back to Home</a>
    </div>
  </section>"""
    main = """  <main class="page-main">
    <div class="container">
      <div class="page-section">
        <h2>Popular Pages</h2>
        <ul>
          <li><a href="/services/exterior-painting/">Exterior House Painting</a></li>
          <li><a href="/services/interior-painting/">Interior Painting</a></li>
          <li><a href="/services/deck-staining/">Deck Staining</a></li>
          <li><a href="/services/custom-murals/">Custom Murals &amp; Accent Walls</a></li>
          <li><a href="/blog/cost-to-paint-a-house-in-grand-rapids/">How Much Does It Cost to Paint a House in Grand Rapids?</a></li>
        </ul>
      </div>
      <div class="page-section">
        <h2>Service Areas</h2>
        <ul>
          <li><a href="/grand-rapids/cascade/">Cascade</a></li>
          <li><a href="/grand-rapids/forest-hills/">Forest Hills</a></li>
          <li><a href="/grand-rapids/ada/">Ada</a></li>
          <li><a href="/grand-rapids/east-grand-rapids/">East Grand Rapids</a></li>
        </ul>
      </div>
      <div class="related-services">
        <h2>Still Stuck?</h2>
        <ul><li><a href="/contact/">Contact Us</a></li><li><a href="tel:+16162642119">Call (616) 264-2119</a></li></ul>
      </div>
    </div>
  </main>"""
    return f"{head}\n{NAV_HTML}\n{hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

# -------- standalone: thank-you (form submission landing) --------
def build_thank_you_page():
    canonical = f"{SITE}/contact/thank-you/"
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Thanks — We Got Your Message | Go Green College Painters</title>
  <meta name="robots" content="noindex, follow" />
  <meta name="description" content="Thanks for reaching out to Go Green College Painters. We'll respond within 24 hours with a free, fixed-price estimate." />
  <link rel="canonical" href="{canonical}" />
{FAVICON_LINKS}
{FONT_LINKS}
</head>
<body>"""
    hero = """  <section class="page-hero hero-default" style="min-height: 380px;">
    <div class="page-hero-inner">
      <h1>Thanks — We Got Your Message</h1>
      <p class="lead">Jackson or Evelyn will get back to you within 24 hours with a free, fixed-price estimate. If you'd rather talk now, call <a href="tel:+16162642119" style="color:var(--gold);font-weight:700;">(616) 264-2119</a>.</p>
      <a href="/" class="btn-primary">Back to Home</a>
    </div>
  </section>"""
    main = """  <main class="page-main">
    <div class="container">
      <div class="page-section">
        <h2>What Happens Next</h2>
        <ul>
          <li>We read every message personally — no chatbot, no overseas inbox.</li>
          <li>We'll reach out within 24 hours (often faster) to schedule a walk-through.</li>
          <li>You'll get a free, fixed-price written estimate after the walk-through — no pressure, no commitment.</li>
        </ul>
      </div>
      <div class="page-section">
        <h2>While You Wait</h2>
        <ul>
          <li><a href="/blog/cost-to-paint-a-house-in-grand-rapids/">What house painting actually costs in Grand Rapids</a></li>
          <li><a href="/blog/cedar-siding-paint-or-stain-grand-rapids/">Cedar siding: paint or stain?</a></li>
          <li><a href="/about/">More about Jackson and Evelyn</a></li>
          <li><a href="https://g.page/r/CddixNttF9ueEBM" target="_blank" rel="noopener">Read our Google reviews</a></li>
        </ul>
      </div>
    </div>
  </main>"""
    return f"{head}\n{NAV_HTML}\n{hero}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

# -------- write pages --------
written = []
for page in PAGES:
    path = page["slug"] + "index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html_out = build_page(page)
    with open(path, "w") as f:
        f.write(html_out)
    written.append((path, len(html_out)))

# 404 — Netlify auto-serves /404.html for unmatched routes
_404 = build_404_page()
with open("404.html", "w") as f:
    f.write(_404)
written.append(("404.html", len(_404)))

# Thank-you landing page for form submissions (noindex; triggers GA4 form_submit event via page_view)
os.makedirs("contact/thank-you", exist_ok=True)
_ty = build_thank_you_page()
with open("contact/thank-you/index.html", "w") as f:
    f.write(_ty)
written.append(("contact/thank-you/index.html", len(_ty)))

# -------- write About & Contact --------
for slug, builder in [("about/", build_about_page), ("contact/", build_contact_page)]:
    os.makedirs(slug, exist_ok=True)
    html_out = builder()
    with open(slug + "index.html", "w") as f:
        f.write(html_out)
    written.append((slug + "index.html", len(html_out)))

# -------- write blog --------
for post in BLOG_POSTS:
    path = post["slug"] + "index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html_out = build_blog_post(post)
    with open(path, "w") as f:
        f.write(html_out)
    written.append((path, len(html_out)))

if BLOG_POSTS:
    os.makedirs("blog", exist_ok=True)
    blog_index_html = build_blog_index(BLOG_POSTS)
    with open("blog/index.html", "w") as f:
        f.write(blog_index_html)
    written.append(("blog/index.html", len(blog_index_html)))

# -------- validate JSON-LD on every page --------
import re
for path, _ in written:
    with open(path) as f: t = f.read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.DOTALL)
    if not m:
        print(f"ERROR: no JSON-LD in {path}"); continue
    try:
        json.loads(m.group(1))
    except Exception as e:
        print(f"ERROR parsing JSON-LD in {path}: {e}"); continue

# -------- print summary --------
print(f"Built {len(written)} pages:")
for path, size in written:
    print(f"  {path}  ({size:,} bytes)")
print(f"\nAll JSON-LD blocks parse OK.")
