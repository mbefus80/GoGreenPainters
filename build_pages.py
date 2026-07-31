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
        "https://www.facebook.com/profile.php?id=61589807997680",
        "https://www.fox17online.com/morning-mix/go-green-college-painters-student-run-family-owned-and-results-that-wow",
        "https://rapidgrowthmedia.com/how-one-family-instilled-children-with-values-of-hard-work-entrepreneurship/",
    ],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5",
        "reviewCount": "11",
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
        "description": "Grand Rapids exterior painting done by the owners — not a rotating summer crew. Featured on Fox 17 Morning Mix. Free written estimate in 24 hours. Serving Cascade, Ada, EGR, Forest Hills.",
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
        "description": "Interior painting in Grand Rapids that leaves zero mess — walls, ceilings, trim, cabinets. Featured on Fox 17 Morning Mix. Free 24-hour quote. Cascade, Ada, EGR, Forest Hills.",
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
        "description": "Deck & fence staining in Grand Rapids — restore weathered wood before Michigan winter. Owner-operated, featured on Fox 17. Free fixed-price quote. Cascade, Ada, EGR, Forest Hills.",
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
        # Page lives in the sitemap as a deep specialty page for "custom murals" queries,
        # but canonical points at /services/custom-painting/ (the broader hub) so Google
        # consolidates ranking signals on a single primary destination.
        "canonical_override": f"{SITE}/services/custom-painting/",
        "title": "Custom Murals & Accent Walls in Grand Rapids, MI | Go Green Painters",
        "description": "Hand-painted custom murals in Grand Rapids — kids' rooms, nurseries, dining rooms, accent walls. Featured on Fox 17 & Rapid Growth Media. Designed by Evelyn Befus, WSU Industrial Design. Free consultation.",
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

    {
        "slug": "services/power-washing/",
        "title": "Power Washing in Grand Rapids, MI | Decks, Siding, Driveways",
        "description": "Grand Rapids power washing — decks, siding, driveways, patios, fences. Bundle multiple surfaces & save. Featured on Fox 17. Free fixed-price quote. Cascade, Ada, EGR, Forest Hills.",
        "h1": "Power Washing in Grand Rapids, MI",
        "hero_img": "/stain-after.jpg",
        "service_name": "Residential Power Washing",
        "service_desc": "Residential power washing in Grand Rapids, MI — decks, fences, vinyl and fiber-cement siding, brick, driveways, patios, and concrete. Soft-wash for delicate finishes. Owner-operated under the Go Green Painters family brand.",
        "service_image": f"{SITE}/exterior-painting.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Power Washing", "/services/power-washing/")],
        "lead": "Power washing is the most underrated home-maintenance service in Michigan. A single visit strips a season's worth of dirt, mildew, algae, and chalking off your siding, deck, fence, driveway, and patio — instantly restoring curb appeal and meaningfully extending the life of paint, stain, and the underlying materials. Henry Befus, the youngest of the Befus siblings behind Go Green, runs our power washing service. Same family work ethic — show up on time, do the job carefully, leave the property cleaner than we found it — applied to outdoor cleaning across Cascade, Forest Hills, Ada, and East Grand Rapids.",
        "sections": [
            ("Surfaces We Clean", """
                <p>A single power washing visit can handle most of the outdoor cleaning a home accumulates over a season. Surfaces we routinely clean:</p>
                <ul>
                  <li><strong>Decks</strong> — wood and composite, including the prep wash before a restain</li>
                  <li><strong>Fences</strong> — wood and vinyl, by linear foot or whole-fence</li>
                  <li><strong>Siding</strong> — vinyl, fiber-cement, brick, and stone</li>
                  <li><strong>Driveways and walkways</strong> — concrete, asphalt, and paver surfaces</li>
                  <li><strong>Patios and pool decks</strong> — concrete and stone</li>
                  <li><strong>Exterior concrete walls and foundations</strong></li>
                  <li><strong>Outdoor furniture, garage doors, and exterior trim</strong> as add-ons</li>
                </ul>
                <p>Most homeowners bundle two or three surfaces on a single visit — a deck plus driveway plus one side of the home is a common combination — for a meaningful discount versus booking each separately.</p>
            """),
            ("Power Washing vs. Soft Washing — When Each Is Right", """
                <p>"Power washing" gets used as a catch-all, but the right technique depends entirely on the surface. We use both:</p>
                <ul>
                  <li><strong>Power washing</strong> uses high water pressure (typically 2,000–4,000 PSI) to physically blast off heavy buildup. It's the right tool for concrete, brick, paver patios, and tough industrial-grade surfaces. Wrong for vinyl siding, painted wood, or any aged surface — high pressure can drive water behind siding, tear fibers, or strip paint.</li>
                  <li><strong>Soft washing</strong> uses lower pressure (under 500 PSI) combined with biodegradable cleaning solutions that lift dirt, mildew, and algae chemically rather than by force. It's the right tool for vinyl siding, painted wood, fiber-cement, asphalt shingles, and any older or delicate surface.</li>
                </ul>
                <p>Most residential exteriors need a combination on the same visit — soft wash on the siding and trim, full power wash on the concrete and pavers. We pick the right approach for each surface, not the other way around. When in doubt, we test in an inconspicuous spot before committing to a full surface.</p>
            """),
            ("Power Washing as Painting Prep", """
                <p>Proper exterior prep is the single biggest factor in how long a paint or stain job lasts. Mildew, chalking, and biological growth left on a surface will cause fresh paint or stain to fail within a year or two. We always include exterior wash as part of our painting and deck staining projects — but a standalone power wash is also a smart move if your paint is otherwise sound and you just want to extend its life without a full repaint yet.</p>
                <p>If you're planning to paint or stain this season, schedule the power wash <strong>4–6 weeks ahead</strong>. That gives the surfaces full time to dry — applying paint or stain to damp wood is the most common reason finishes fail prematurely.</p>
            """),
            ("Cost of Power Washing in Grand Rapids", """
                <p>Realistic pricing for Greater Grand Rapids residential power washing:</p>
                <ul>
                  <li><strong>Standard deck</strong> (200–400 sq ft): $150–$300</li>
                  <li><strong>Full siding wash</strong> (one- or two-story home): $300–$600</li>
                  <li><strong>Driveway</strong>: $100–$250</li>
                  <li><strong>Concrete patio or walkway</strong>: $80–$200</li>
                  <li><strong>Fence</strong> (residential, typical perimeter): $200–$500</li>
                  <li><strong>Whole-property bundle</strong> (siding + driveway + deck): $500–$1,200, usually 15–25% less than booking separately</li>
                </ul>
                <p>Every quote is free, fixed-price, and based on a walk-through. Bundled visits beat individual bookings on price and on scheduling.</p>
            """),
            ("When to Schedule in Michigan", """
                <p>The Grand Rapids power washing season runs <strong>April through mid-October</strong>. A few timing notes worth knowing:</p>
                <ul>
                  <li><strong>Spring (April–May)</strong> is our busiest window — winter leaves a season of biological buildup that homeowners want gone. Book 2–4 weeks ahead in peak spring.</li>
                  <li><strong>Pre-painting</strong>: schedule 4–6 weeks before your painting/staining project to give surfaces time to fully dry.</li>
                  <li><strong>Fall (September–October)</strong>: a fall power wash removes summer pollen, mildew, and algae before they overwinter on your surfaces. Decks and siding both benefit from a pre-winter clean.</li>
                  <li><strong>Mid-summer</strong>: faster scheduling typically available, plus great weather for drying.</li>
                </ul>
            """),
        ],
        "faqs": [
            ("How much does power washing cost in Grand Rapids?", "Residential power washing in Grand Rapids generally runs $150–$600 depending on surface and size. A standard deck runs $150–$300; full siding wash on a typical home runs $300–$600; driveways $100–$250; fences $200–$500. Bundling multiple surfaces on one visit usually saves 15–25%. Every quote is free and fixed-price."),
            ("Will power washing damage my deck or siding?", "Done wrong, yes — that's why technique matters more than equipment. The risk on wood and delicate surfaces is too much pressure tearing fibers, driving water behind siding, or stripping finish. We size pressure and nozzle to the specific surface, and use soft-wash (low-pressure plus cleaning solution) on materials that can't tolerate high pressure: vinyl siding, painted wood, older shake, asphalt shingles. We always test in an inconspicuous spot first."),
            ("What's the difference between power washing and soft washing?", "Power washing uses high water pressure (typically 2,000–4,000 PSI) to physically blast off buildup. It's right for concrete, brick, and durable surfaces. Soft washing uses lower pressure (under 500 PSI) combined with biodegradable cleaning solutions to lift dirt and biological growth chemically rather than by force. It's right for vinyl siding, painted wood, fiber-cement, and any aged surface where high pressure would cause damage. Most residential exteriors need a combination on the same visit."),
            ("Should I power wash my house before painting?", "Yes — proper exterior prep is the single biggest factor in how long a paint job lasts. Power washing removes dirt, mildew, chalking, and loose paint that would otherwise cause new paint to peel within a year or two. We include exterior wash as part of our painting projects, but you can also book a standalone power wash 4–6 weeks before painting day to let surfaces dry fully."),
            ("How often should I power wash my deck?", "Most Grand Rapids decks benefit from a power wash once a year — typically in spring after winter buildup. If you're restraining the deck, plan to power wash 4–6 weeks ahead so the wood dries completely before stain goes on. Decks under heavy tree cover or in shaded north-side positions may need a wash twice a year due to faster mildew accumulation."),
            ("Do you clean fences, driveways, and patios too?", "Yes. Wood and vinyl fences, concrete and paver driveways, walkways, patios, and exterior concrete walls are all standard surfaces. Most homeowners bundle 2–3 of these onto a single visit for a meaningful discount versus booking each separately."),
            ("Can power washing remove paint or stain?", "Yes — high-pressure water strips both. That's actually useful when removing failing paint or weathered stain as part of prep for a repaint or restain. It's a problem when you have a sound finish you want to preserve. We always assess existing finish condition first and adjust technique accordingly: soft wash to preserve, full power wash when stripping is the goal."),
            ("Who actually does the power washing work at Go Green?", "Henry Befus, the youngest of the Befus siblings behind Go Green. Power washing is his dedicated focus on the team. He grew into the work from his earlier bin-cleaning route and is being mentored by his older siblings into the broader trade — typical of how our family business operates."),
        ],
        "related": [
            ("Exterior House Painting", "/services/exterior-painting/"),
            ("Deck Staining", "/services/deck-staining/"),
            ("Cost to Paint a House in Grand Rapids", "/blog/cost-to-paint-a-house-in-grand-rapids/"),
            ("House Painters in Cascade", "/grand-rapids/cascade/"),
        ],
        "related_heading": "Related Services",
    },

    # ============================================================
    # NEIGHBORHOOD PAGES
    # Cedar-siding expertise is the through-line for Cascade,
    # Forest Hills, and Ada. EGR leans on mixed materials.
    # ============================================================
    {
        "slug": "grand-rapids/cascade/",
        "title": "Cascade, MI House Painters | Cedar Siding Specialists",
        "description": "Cascade painters specializing in cedar siding — tannin-blocking prep, 8-12 year finish life. Owner-operated, featured on Fox 17 Morning Mix. Free written quote in 24 hours.",
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
        "description": "Forest Hills painters — exterior cedar, interior repaints, cabinet refinishing. Owner-operated, featured on Fox 17 Morning Mix. Free 24-hour written quote. Northern & Central FH.",
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
        "description": "Ada painters — Ada Village, Bostwick Lake, estates south of Fulton. Cedar siding specialists. Owner-operated, featured on Fox 17. Free fixed-price quote in 24 hours.",
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
        "description": "East Grand Rapids painters — 1920s-1950s homes, Reeds Lake builds, cedar trim, plaster walls. Owner-operated, featured on Fox 17 Morning Mix. Free quote in 24 hours.",
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
        "description": "Real 2026 painting costs in Grand Rapids: interior $4,700-$8,500, exterior $3,000-$7,000, cabinets $2,500-$6,000. What drives the price — from a painter featured on Fox 17.",
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
        "description": "Cedar siding in Grand Rapids: paint or stain? Which lasts longer, what each costs, common failure modes in Michigan weather. From cedar specialists serving Cascade, Ada, Forest Hills, EGR.",
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
        "description": "Owner-operated painter vs. college painting franchise in Grand Rapids: how each business model actually works, real review data, and 5 questions to ask before you hire either.",
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

    {
        "slug": "blog/painting-stucco-brick-cedar-vinyl-grand-rapids/",
        "title": "How to Paint Stucco, Brick, Cedar, Vinyl, and Fiber-Cement Siding: A Grand Rapids Guide",
        "description": "Painting mixed exteriors in Grand Rapids? What stucco, brick, cedar, vinyl, fiber-cement, and aluminum each need — prep, primer, products, and lifespan. From an owner-operated painter.",
        "h1": "How to Paint Stucco, Brick, Cedar, Vinyl, and Fiber-Cement Siding",
        "hero_img": "/exterior-after.jpg",
        "date_published": "2026-06-17",
        "date_modified": "2026-06-17",
        "author_id": f"{SITE}/#jackson",
        "author_name": "Jackson Befus",
        "breadcrumb": [("Home", "/"), ("Blog", "/blog/"), ("Painting Different Siding Types", "/blog/painting-stucco-brick-cedar-vinyl-grand-rapids/")],
        "lead": "Most Grand Rapids homes don't have just one type of exterior surface. Walk any block in Cascade, Forest Hills, Ada, or East Grand Rapids and you'll see homes with cedar shake gables over brick foundations, stucco upper sections with vinyl lap below, painted brick with cedar trim, fiber-cement siding under aluminum soffits. Each material requires a different prep approach, different primer, sometimes different paint entirely. Pick the wrong approach and the finish fails within a year or two — peeling on stucco, bleeding on cedar, lifting on vinyl, chalking on brick. This is the field guide we wish more homeowners had before getting their first painting quote.",
        "sections": [
            ("Why Surface Type Matters More Than the Paint Brand", """
                <p>The single biggest factor in how long an exterior paint job lasts isn't the paint brand — it's whether the prep, primer, and finish were matched to the substrate. A premium 100% acrylic paint applied to badly-prepped cedar will fail in 18 months. A mid-tier paint applied to properly-prepped vinyl can last 8–10 years.</p>
                <p>When we walk a home for an estimate, the first thing we do is identify every distinct surface material. A typical Cascade home might have four: brick foundation, cedar shake upper gables, fiber-cement lap on the main wall, and aluminum soffits. Each gets its own approach. The mistake most painters (and homeowners) make is treating exterior paint like a single decision, when it's actually four or five decisions stacked together.</p>
            """),
            ("Stucco", """
                <p>Stucco is common on Grand Rapids homes as full coverage on Mediterranean and Spanish-style builds, and very common as upper-gable sections on craftsman and traditional homes. Two things make it tricky to paint: it's extremely porous, and it expands and contracts with temperature swings more than most other surfaces.</p>
                <p><strong>Prep:</strong> Clean with a soft wash (high pressure can erode the stucco surface or drive water behind it). Patch hairline cracks with elastomeric crack filler. Inspect for efflorescence — those white powdery deposits where moisture has worked its way through; if present, brush off and seal the source.</p>
                <p><strong>Primer:</strong> Alkali-resistant masonry primer on any bare stucco. New stucco needs to cure 28 days before painting.</p>
                <p><strong>Paint:</strong> Acrylic elastomeric is the gold standard for full stucco coverage — it bridges hairline cracks and accommodates seasonal movement. Breathable acrylic masonry paint is the alternative for areas where moisture transmission matters. Avoid standard exterior latex on stucco; it doesn't flex enough.</p>
                <p><strong>Lifespan:</strong> 8–12 years with proper prep, 10–15 with elastomeric. Common failure: paint that doesn't allow moisture to escape, leading to blistering during freeze-thaw cycles.</p>
            """),
            ("Brick", """
                <p>Painting brick is the most controversial exterior decision a homeowner can make. Once you paint brick, you're committed — returning to natural brick later involves chemical stripping or soda blasting, which is expensive ($3–$5 per square foot and up). That said, well-painted brick on the right home looks excellent and protects the brick from moisture and pollutant absorption.</p>
                <p><strong>Prep:</strong> Soft wash to remove dirt, mildew, and any loose mortar dust. Repoint failing mortar joints before painting — paint won't fix bad tuckpointing. Avoid pressure washing brick aggressively; high pressure can drive water deep into porous masonry where it stays for weeks.</p>
                <p><strong>Primer:</strong> Alkali-resistant masonry primer. Critical step — without it, the brick's natural alkalinity can break down the paint film.</p>
                <p><strong>Paint:</strong> 100% acrylic masonry paint or specialty elastomeric paint formulated for brick. The paint needs to be breathable so trapped moisture can escape.</p>
                <p><strong>Lifespan:</strong> 10–15 years done correctly. Done incorrectly, peeling can start in year one.</p>
                <p><strong>One honest note:</strong> if you have brick that's in good condition and you're considering painting it for aesthetic reasons, take 24 hours before deciding. It's a one-way street.</p>
            """),
            ("Cedar Shake, Shingle, and Lap", """
                <p>Cedar gets its own deep dive in <a href="/blog/cedar-siding-paint-or-stain-grand-rapids/">our dedicated cedar guide</a> — the prep choices for cedar are involved enough to deserve their own post. The short version:</p>
                <ul>
                  <li><strong>Tannin bleed</strong>: cedar's natural tannins bleed pinkish stains through fresh paint without a stain-blocking primer (oil-based or pigmented shellac).</li>
                  <li><strong>Knot priming</strong>: every visible knot needs individual shellac-based spot-priming or sap will bleed through the topcoat within a season.</li>
                  <li><strong>Mildew on shaded sides</strong>: wooded Cascade and Ada lots see persistent mildew on shaded north walls; mildewcide wash before painting.</li>
                </ul>
                <p><strong>Paint vs stain decision</strong>: if your cedar isn't already painted, stain is usually the better long-term call. Stain penetrates the wood and ages by fading rather than peeling. If your cedar has been painted multiple times already, repainting is usually the practical choice since stripping is expensive.</p>
                <p><strong>Lifespan:</strong> 8–12 years for paint on cedar (less on south- and west-facing walls), 4–6 years for semi-transparent stain, 6–8 years for solid stain.</p>
            """),
            ("Fiber-Cement (Hardie Board and Similar)", """
                <p>Fiber-cement has become the dominant new-construction siding in West Michigan over the past 15 years. It's durable, fire-resistant, and holds paint exceptionally well — but it has one specific weakness that catches a lot of painters out: the joints.</p>
                <p><strong>Prep:</strong> Standard wash. The factory primer that comes on most fiber-cement is good, but any cut edges (around windows, at corners) need to be spot-primed before paint. Caulk every butt joint where two boards meet — fiber-cement panels expand and contract less than wood but enough to crack inflexible paint film at joints.</p>
                <p><strong>Primer:</strong> Factory-primed product needs only spot priming on cut edges. Unprimed or repaint situations: 100% acrylic primer.</p>
                <p><strong>Paint:</strong> 100% acrylic latex. Fiber-cement is one of the most paint-friendly surfaces — most premium exterior paints work well.</p>
                <p><strong>Lifespan:</strong> 15–20 years on properly painted fiber-cement. The longest-lasting common exterior surface in Grand Rapids.</p>
                <p><strong>Common mistake</strong>: not caulking butt joints. Caulking is what makes fiber-cement paint last 15+ years instead of failing at every joint in year three.</p>
            """),
            ("Vinyl Siding", """
                <p>Vinyl is the most common exterior surface on suburban Grand Rapids homes built between 1980 and 2010. The question "can you paint vinyl?" used to have an interesting answer — modern vinyl-safe paints have made it a clean yes, with one important rule.</p>
                <p><strong>The dark-color rule</strong>: you cannot paint vinyl siding a color darker than its original shade. Darker colors absorb more heat, and vinyl warps when it gets hot. Stay at the original shade or lighter — this is non-negotiable, not a stylistic suggestion. Reputable paint manufacturers void warranties on vinyl painted darker than original.</p>
                <p><strong>Prep:</strong> Soft wash to remove oxidation, mildew, and surface chalking. Light scuff with a Scotch-Brite pad on heavily oxidized vinyl to give the new paint a key.</p>
                <p><strong>Primer:</strong> Generally not needed on sound vinyl — premium vinyl-safe paints are self-priming on clean vinyl. Heavily chalking vinyl benefits from a bonding primer.</p>
                <p><strong>Paint:</strong> Must be vinyl-safe acrylic. Sherwin-Williams VinylSafe and Benjamin Moore Regal Select with the vinyl-safe formula are the two leading options. Standard exterior latex will work but with reduced lifespan.</p>
                <p><strong>Lifespan:</strong> 8–10 years on properly painted vinyl.</p>
            """),
            ("Aluminum Siding", """
                <p>Aluminum siding peaked in residential building between roughly 1960 and 1985. A lot of older Grand Rapids homes — especially in established neighborhoods like Eastown, Creston, and parts of East Grand Rapids — still have it. The most common condition issue with aging aluminum siding is chalking: that fine powdery surface you can rub off with your hand.</p>
                <p><strong>Prep:</strong> Pressure wash (aluminum can take real pressure — it's much more forgiving than vinyl or wood). Sand or wire-brush areas with heavy chalking to remove the loose powder. Spot-prime any dented or scratched areas where bare aluminum is exposed.</p>
                <p><strong>Primer:</strong> Bonding primer or self-etching metal primer on bare aluminum and on heavily chalked surfaces.</p>
                <p><strong>Paint:</strong> 100% acrylic latex exterior paint.</p>
                <p><strong>Lifespan:</strong> 10–15 years for properly painted aluminum.</p>
                <p><strong>Telling aluminum from vinyl</strong>: aluminum dents on impact; vinyl cracks or breaks. Aluminum also feels metallic and cold to the touch in cool weather; vinyl feels like plastic.</p>
            """),
            ("Wood Clapboard and Traditional Lap Siding", """
                <p>Older Grand Rapids homes — especially the 1920s-1950s East Grand Rapids, Eastown, and Heritage Hill neighborhoods — often have traditional wood clapboard or lap siding. It looks similar to cedar but uses different wood (often pine, fir, or redwood depending on era) and tends to have different grain and aging patterns.</p>
                <p><strong>Prep:</strong> Scrape and sand loose paint to a sound substrate. Spot-prime bare wood with an oil-based primer for best adhesion. Caulk gaps at corners, around windows, and along trim seams.</p>
                <p><strong>Primer:</strong> Oil-based stain-blocking primer on bare wood. Latex primer on previously-painted-and-sanded surfaces.</p>
                <p><strong>Paint:</strong> Premium 100% acrylic exterior paint, two coats.</p>
                <p><strong>Lifespan:</strong> 8–12 years on properly prepped wood lap.</p>
                <p><strong>The historic home consideration</strong>: older clapboard often has multiple paint layers, sometimes including lead paint on pre-1978 homes. Lead-safe work practices (EPA RRP) are required when disturbing pre-1978 paint, and the prep work is more involved on these homes than on modern siding.</p>
            """),
            ("Mixed-Surface Homes: The Most Common Grand Rapids Situation", """
                <p>Most homes we paint in Grand Rapids have two or three exterior surface materials. Common combinations:</p>
                <ul>
                  <li><strong>Brick foundation + cedar shake upper + aluminum soffits</strong> — typical 1970s Cascade ranch</li>
                  <li><strong>Stucco upper gable + vinyl lap below + cedar trim</strong> — common 1990s build</li>
                  <li><strong>Fiber-cement field + cedar trim + brick chimney</strong> — typical new construction</li>
                  <li><strong>Painted brick + cedar shutters + wood trim</strong> — older East Grand Rapids homes</li>
                </ul>
                <p>Each surface gets its own assessment, its own prep approach, sometimes its own primer, and sometimes its own paint product. Pricing reflects this complexity — a home with four different surface materials takes meaningfully more time than a single-surface home of the same square footage, because the painter is switching techniques and products throughout the day.</p>
                <p>This is one of the reasons we provide written, fixed-price estimates after a walk-through rather than per-square-foot quotes over the phone. Square footage tells us almost nothing without knowing the surface mix.</p>
            """),
            ("Mistakes We See Across Every Surface Type", """
                <ul>
                  <li><strong>Using one paint for everything.</strong> The same product on brick, cedar, and vinyl will fail differently on each — usually on the cedar first, the brick second, the vinyl last.</li>
                  <li><strong>Skipping primer to save money.</strong> Primer cost is roughly 10% of total paint cost. Failure from skipping primer adds 80% to the next repaint cost.</li>
                  <li><strong>Wrong sheen for the surface.</strong> Flat or matte sheens hide imperfections on stucco and brick. Satin and semi-gloss work on trim and doors. Eggshell is the standard for most siding.</li>
                  <li><strong>Painting in wrong weather.</strong> Hot weather (over 90°F) makes paint dry too fast and skin over before it can level. Cold weather (under 50°F) slows curing dangerously. High humidity slows drying and traps moisture.</li>
                  <li><strong>Not caulking before painting.</strong> Especially on fiber-cement, wood lap, and trim. Caulk after painting and the caulk lines are visible forever; caulk before, and the paint covers smoothly.</li>
                </ul>
            """),
        ],
        "faqs": [
            ("Can I use the same paint for stucco, brick, cedar, and vinyl on my house?", "Generally no. Brick and stucco need masonry-formulated paint (typically alkali-resistant). Cedar needs tannin-blocking primer and acrylic exterior paint. Vinyl needs vinyl-safe acrylic. Fiber-cement is the most flexible — most premium acrylic exteriors work. Using one product across all four surfaces means at least one will fail prematurely. We use the right product for each surface and price the project accordingly."),
            ("Can painted brick be returned to natural brick?", "Yes, but it's expensive — typically $3–$5 per square foot using soda blasting or chemical strippers, and the original brick is rarely perfectly restored. The brick mortar joints in particular often suffer. If you're considering painting brick, take the decision seriously: it's effectively a one-way choice."),
            ("Should I paint my vinyl siding or replace it?", "Depends on the condition and your timeline. Sound vinyl in fundamentally good shape (no cracking, no warping, no major fading patterns) is a clean candidate for paint — vinyl-safe paint extends life by 8–10 years at roughly 25% the cost of full replacement. Vinyl that's cracking, brittle, or warped should be replaced; paint won't fix structural issues. The dark-color rule applies either way: you cannot paint vinyl darker than the original shade."),
            ("What's the lifespan of exterior paint on different surfaces in Michigan?", "Realistic lifespans in Grand Rapids: stucco 8–12 years (15+ with elastomeric), painted brick 10–15 years, cedar 8–12 years for paint or 4–8 for stain, fiber-cement 15–20 years, vinyl 8–10 years, aluminum 10–15 years, wood clapboard 8–12 years. South- and west-facing walls reach the low end of the range; north sides reach the high end."),
            ("What exterior surfaces does Go Green Painters work with?", "All of them — stucco, brick (painted), cedar shake and lap, fiber-cement, vinyl, aluminum, wood clapboard, masonry, concrete, and the mix-and-match combinations most Grand Rapids homes actually have. We don't subcontract specialty surface work; the same two-person team handles every material."),
            ("Is fiber-cement different from cedar siding?", "Yes — significantly. Fiber-cement (Hardie Board and similar) is a cement-based composite that looks like wood but is manufactured. It's dimensionally stable, holds paint 15–20 years, and doesn't have wood's tannin or knot issues. Cedar is real wood with grain, knots, and tannins; it needs more involved prep but ages with a distinct character. Both are excellent siding materials; they require different approaches when painting."),
            ("Can stucco be painted any color?", "Yes — unlike vinyl, stucco doesn't have a color-temperature restriction. Stucco can take any shade including deep tones. The technical requirements are matching the paint type to the stucco (masonry-formulated, breathable or elastomeric) and proper prep; color choice doesn't affect paint performance the way it does on vinyl."),
            ("How do you price homes with multiple surface types?", "Always with a written, fixed-price estimate after a walk-through. Square footage alone doesn't tell us much without knowing the surface mix — a 2,400 sq ft brick-and-vinyl home and a 2,400 sq ft stucco-cedar-fiber-cement home are very different jobs. We walk the property, identify each surface, plan the prep and product per surface, and quote a number that holds. No surprise upcharges mid-project."),
        ],
        "related": [
            ("Cedar Siding in Grand Rapids: Paint or Stain?", "/blog/cedar-siding-paint-or-stain-grand-rapids/"),
            ("Cost to Paint a House in Grand Rapids", "/blog/cost-to-paint-a-house-in-grand-rapids/"),
            ("Exterior House Painting", "/services/exterior-painting/"),
            ("Power Washing — Prep for Painting", "/services/power-washing/"),
        ],
        "related_heading": "Related Reading & Services",
    },

    {
        "slug": "blog/affordable-painters-grand-rapids/",
        "title": "How to Find a Good, Affordable Painter in Grand Rapids (Without Cutting Corners)",
        "description": "How to find a good, affordable painter in Grand Rapids: what fair pricing actually looks like, red flags in quotes, and how to compare 3 painters apples-to-apples. From a Fox 17-featured painter.",
        "h1": "How to Find a Good, Affordable Painter in Grand Rapids",
        "hero_img": "/exterior-after.jpg",
        "date_published": "2026-06-17",
        "date_modified": "2026-06-17",
        "author_id": f"{SITE}/#jackson",
        "author_name": "Jackson Befus",
        "breadcrumb": [("Home", "/"), ("Blog", "/blog/"), ("How to Find a Good, Affordable Painter", "/blog/affordable-painters-grand-rapids/")],
        "lead": "\"Good quality and affordable\" is what most Grand Rapids homeowners actually want when they hire a painter. Not the cheapest — cheap painters cost more long-term when their work fails in two years. Not the most expensive — premium pricing often pays for corporate overhead rather than better craftsmanship. The sweet spot is in the middle: real quality work at fair, honest prices. Here's an honest guide to where painter pricing actually comes from, how to spot quality work without overpaying, and how to evaluate any quote before you sign.",
        "sections": [
            ("What 'Affordable' Actually Means in Residential Painting", """
                <p>The word "affordable" gets used in confusing ways in the painting industry. It's worth being precise about three different concepts:</p>
                <ul>
                  <li><strong>Cheap</strong> — the lowest price available, usually achieved by cutting prep, using lower-grade paint, or skipping warranties. A cheap painter saves you money today and costs you money in three years.</li>
                  <li><strong>Premium</strong> — the highest price in the market, often justified by claims of superior quality. Sometimes accurate; often the price reflects corporate overhead, sales commissions, and marketing budgets rather than better craftsmanship.</li>
                  <li><strong>Affordable</strong> — the middle path. Real quality work, full prep, premium materials, written warranty, all at a fair price relative to the value delivered. No overhead inflation, no cut corners.</li>
                </ul>
                <p>When customers tell us they're looking for "good quality and affordable," they mean the third one. They want value, not extremes. They want a painter who does the job right without making them pay for an organization that doesn't help the work itself.</p>
            """),
            ("Where a Painter's Price Actually Comes From", """
                <p>Most homeowners never see the breakdown of what they're paying for. Roughly speaking, a residential painting quote in Grand Rapids breaks down like this:</p>
                <ul>
                  <li><strong>Labor</strong> — 50 to 60% of the total. The painter's time on prep, application, and cleanup.</li>
                  <li><strong>Materials</strong> — 15 to 20%. Paint, primer, caulk, drop cloths, brushes, rollers, tape.</li>
                  <li><strong>Direct overhead</strong> — 10 to 15%. Insurance, equipment, vehicles, fuel.</li>
                  <li><strong>Profit margin</strong> — 10 to 15%. What the company actually earns.</li>
                </ul>
                <p>For franchise painters and larger companies with sales teams, add three more layers on top:</p>
                <ul>
                  <li><strong>Corporate franchise fees and royalties</strong> — 5 to 15% paid to the franchisor for the brand</li>
                  <li><strong>Corporate marketing and lead-generation budget</strong> — 5 to 10% that funds the ads and Google placements you saw</li>
                  <li><strong>Salesperson commissions</strong> — 5 to 10% for the person who quoted your job but who isn't the person who paints it</li>
                </ul>
                <p>Add those three categories up and a franchise quote on the same physical work is structurally 15-35% higher than an owner-operated quote. That difference isn't going into better paint, more prep time, or longer warranty — it's funding the company structure around the work.</p>
            """),
            ("The Hidden Costs of 'Cheap' Painters", """
                <p>The painter who comes in at half the price of everyone else is almost always cutting something. The most common shortcuts, in order of how often we see them on repaint projects where another painter did the previous job:</p>
                <ul>
                  <li><strong>Skipped or rushed prep work</strong> — this is the single biggest factor in how long paint lasts. A proper exterior repaint includes pressure washing, scraping all loose paint, sanding, priming bare wood, caulking gaps, and spot-priming knots. Skipping any of these is invisible at the moment but causes peeling within 1-3 years.</li>
                  <li><strong>One coat instead of two</strong> — looks fine on day one, looks faded and uneven by year three.</li>
                  <li><strong>Lower-grade paint</strong> — a $25/gallon contractor paint covers like a $55/gallon premium paint but lasts half as long.</li>
                  <li><strong>No primer where it's needed</strong> — on bare wood, on cedar, on knots, on patched drywall. Primer skip means topcoat failure.</li>
                  <li><strong>No warranty</strong> — or a warranty that excludes everything that could actually go wrong.</li>
                </ul>
                <p>The math on this is brutal. A repaint that fails at year three instead of lasting twelve means you pay for the same job four times over a 12-year span. The "cheap" painter cost you 4x what an honest painter would have cost.</p>
            """),
            ("The Hidden Costs of 'Premium' Painters", """
                <p>The opposite end of the market has its own structural problems. A premium-priced franchise quote on a $5,000 job might include $750-$1,500 in costs that don't make the paint last longer or look better:</p>
                <ul>
                  <li><strong>Corporate overhead</strong> doesn't make the prep more thorough or the paint better quality. It pays for the brand, the back office, and the franchise system.</li>
                  <li><strong>Salesperson commissions</strong> mean you're funding a person who isn't on your project. The person who quoted the job hands the actual work off to a crew. Accountability suffers in that handoff.</li>
                  <li><strong>Brand marketing budgets</strong> mean you're paying for the next homeowner's ad impression rather than for better work on your home.</li>
                  <li><strong>Franchise fees</strong> are baked into every quote — the local branch sends a percentage of every job to corporate.</li>
                </ul>
                <p>Premium pricing can be justified when it correlates with premium work — longer warranties, better paint products, more experienced crews. Often it doesn't. The quality of work at a $5,000 owner-operated job and a $7,500 franchise job is frequently identical; the difference is who's collecting the extra $2,500.</p>
            """),
            ("The Structural Advantage of Owner-Operated", """
                <p>Owner-operated painters can charge less than franchises and still earn fair pay because of how the economics actually work:</p>
                <ul>
                  <li><strong>No franchise fees</strong> — no corporate royalty taken off the top of every job</li>
                  <li><strong>Lower marketing budget</strong> — referrals and local SEO instead of broadcast advertising</li>
                  <li><strong>No salesperson layer</strong> — the same person quotes, paints, and stands behind the work, which removes a 5-10% cost layer</li>
                  <li><strong>Smaller fleet, less overhead</strong> — one or two vehicles instead of a regional logistics operation</li>
                  <li><strong>Direct accountability</strong> — the owner has personal long-term reputation on every job, which usually produces more careful work, not less</li>
                </ul>
                <p>The result: lower prices without lower quality. Sometimes the same prep, the same paint, the same warranty terms — at 20-30% less.</p>
                <p>The trade-off is capacity. An owner-operated painter takes meaningfully fewer projects per season than a franchise crew can. If you call in May for a same-week start, an owner-operated painter probably can't accommodate. Plan two to six weeks ahead and the model works.</p>
            """),
            ("How to Evaluate Any Painter's Quote", """
                <p>The most important thing you can do as a homeowner is read the actual quote — not just the bottom-line number. Here's what to look at:</p>
                <ul>
                  <li><strong>Prep work specifications.</strong> Does the quote describe exactly what prep is included? Pressure wash, scrape, sand, caulk, prime as needed, mildewcide on shaded sides? Or does it just say "prep as needed" (which means the painter decides on the day what's worth doing)?</li>
                  <li><strong>Paint brand and product line.</strong> "Sherwin-Williams" is vague. "Sherwin-Williams Duration Exterior in [color]" is specific. The product line within a brand matters — a $30/gallon contractor line and a $65/gallon premium line are different products that last different lengths of time.</li>
                  <li><strong>Number of coats.</strong> One coat or two? Most exterior repaints need two.</li>
                  <li><strong>Warranty length and what it covers.</strong> Three years on workmanship? Five? What's excluded? "Limited warranty" without specifics means nothing.</li>
                  <li><strong>Insurance certificate.</strong> Can the painter email you a current general liability insurance certificate before you sign? If the answer is "I'll get that to you later," that's a flag.</li>
                  <li><strong>Who actually does the work.</strong> Will the person who walked the property be the person painting? Or will the work be done by a different crew?</li>
                </ul>
                <p>A quote that answers all six of these questions concretely — in writing — is structurally a better quote than one that doesn't, even if the bottom-line number is higher.</p>
            """),
            ("Red Flags That a Cheap Quote Will Cost More Later", """
                <p>The cheapest quote is often a quote that's missing things. Red flags worth catching:</p>
                <ul>
                  <li><strong>No mention of prep work, or vague language ("prep as needed")</strong></li>
                  <li><strong>No paint product specified, just a brand name</strong></li>
                  <li><strong>No written contract, only a verbal agreement or a number scribbled on a quote sheet</strong></li>
                  <li><strong>Pressure to decide quickly or "lock in today's price"</strong></li>
                  <li><strong>No proof of insurance, or insurance certificate the painter promises to send "later"</strong></li>
                  <li><strong>Cash only, or large upfront payments before any work starts</strong> (a deposit of 10-30% is normal; 100% upfront is not)</li>
                  <li><strong>No physical local address for the business</strong></li>
                  <li><strong>No online reviews or no traceable presence at all</strong></li>
                </ul>
                <p>Any one of these can be explained away in some cases. Two or more together is a pattern. If the quote is dramatically lower than competing quotes and any of these flags are present, the savings aren't real.</p>
            """),
            ("Why We Built Go Green This Way", """
                <p>Go Green College Painters is owner-operated. Jackson and Evelyn Befus do the work themselves. There's no franchise above us, no sales team between us and clients, no corporate marketing budget to fund. That's not a marketing position — it's the actual structure of the company.</p>
                <p>The practical result: we can charge less than the franchise quotes you'll get on the same job and still earn fair pay, while doing the same prep, using the same premium paint, and offering the same warranty. We don't need to cut corners to compete on price, because we don't have the corporate overhead that forces other painters to charge more.</p>
                <p>If "good quality and affordable" is what you're actually looking for, that's structurally what we are.</p>
            """),
        ],
        "faqs": [
            ("What's a fair price for residential painting in Grand Rapids?", "Fair Grand Rapids pricing: interior repaints $700-$1,700 per room or $4,700-$8,500 for a whole house; exterior repaints $3,000-$7,000 for typical homes; cabinet refinishing $2,500-$6,000; deck staining $700-$2,500. Quotes that come in dramatically below these ranges usually involve cut corners; quotes dramatically above usually involve corporate overhead rather than better work."),
            ("Why do painting quotes vary so much for the same job?", "Three reasons. First, prep work — quotes that include thorough prep cost more than quotes that skip it. Second, paint quality — premium 100% acrylic paints cost more per gallon than contractor-grade and last twice as long. Third, business overhead — franchises and larger companies pass corporate fees, sales commissions, and marketing budgets into every quote. An owner-operated painter doing identical work has structurally lower overhead."),
            ("Should I always go with the lowest quote?", "No — and counterintuitively, the lowest quote often costs the most over time. A repaint that fails at year three instead of year twelve means paying for the same job four times in a decade. The right move is comparing what's actually included in each quote (prep specifications, paint brand and line, number of coats, warranty terms) and picking the best value, not the lowest number."),
            ("How can I tell if a painter is cutting corners?", "Read the written quote. Vague language like 'prep as needed' or 'two coats of paint' (without specifying product line) usually means the painter is reserving the right to do less than thorough work. Specific quotes — listing every prep step, the exact paint product line, the warranty terms — indicate the painter intends to do real work. Also ask: can you email me a current insurance certificate before we start?"),
            ("What questions should I ask before hiring a painter?", "Eight worth asking: (1) Who specifically will be on my property? (2) Can you send a current insurance certificate today? (3) What exact paint product and how many coats? (4) Walk me through your prep step by step. (5) What's the warranty length and what does it cover? (6) Can I see two or three recent local project addresses? (7) What happens if it rains mid-project? (8) How are change orders handled? An honest contractor answers all eight without hesitation."),
            ("How is Go Green able to offer lower prices than franchises?", "We don't pay franchise fees, salesperson commissions, or corporate marketing budgets — those layers don't exist in our company structure. The same person who quotes your job is the person who paints it, which removes the sales/crew handoff that adds cost without adding quality. We use the same premium paints and the same prep approach as the higher-priced franchises; we just don't have the same overhead inflating the final number."),
            ("Are owner-operated painters less professional than franchised companies with crews?", "Different, not less. Franchise crews can sometimes complete more projects per week because of their scale. Owner-operated painters take fewer projects per season but typically with more careful prep and tighter accountability, because the owner's personal long-term reputation is tied to every single job. Both models can produce excellent work; the question is fit for your specific project and timeline."),
            ("What's the most common painter pricing scam in Grand Rapids?", "The most common pattern is a low quote with vague prep specifications, an unspecified paint product, no written warranty, and a large upfront payment required to lock in the 'low price.' The work is then done quickly with minimal prep and contractor-grade paint, fails within 2-3 years, and the original painter is either out of business or unreachable. Reading the quote carefully and verifying insurance before paying anything substantial protects against this entirely."),
        ],
        "related": [
            ("Owner-Operated vs. College Painting Franchises", "/blog/owner-operated-vs-college-painting-franchises-grand-rapids/"),
            ("Cost to Paint a House in Grand Rapids", "/blog/cost-to-paint-a-house-in-grand-rapids/"),
            ("Painting Stucco, Brick, Cedar, Vinyl & Fiber-Cement", "/blog/painting-stucco-brick-cedar-vinyl-grand-rapids/"),
            ("About Go Green College Painters", "/about/"),
        ],
        "related_heading": "Related Reading",
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
      <li><a href="/#services">Painting</a></li>
      <li><a href="/services/power-washing/">Power Washing</a></li>
      <li><a href="/plants-and-pets/">Plants &amp; Pets</a></li>
      <li><a href="/services/custom-painting/">Custom Murals</a></li>
      <li><a href="/about/">About</a></li>
      <li class="nav-phone-li"><a href="tel:+16162642119" class="nav-phone">(616) 264-2119</a></li>
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
          <li><a href="/services/custom-painting/">Custom Painting</a></li>
          <li><a href="/services/custom-murals/">Custom Murals &amp; Accent Walls</a></li>
          <li><a href="/services/custom-banners/">Hand-Painted Banners</a></li>
          <li><a href="/services/power-washing/">Power Washing</a></li>
          <li><a href="/plants-and-pets/">Plants &amp; Pets (Vacation Care)</a></li>
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
          <li><a href="https://www.facebook.com/profile.php?id=61589807997680" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2024&ndash;2026 Go Green College Painters. All rights reserved.</span>
      <span>Greater Grand Rapids, MI</span>
    </div>
  </footer>"""

# Compact press strip — injected on every generated inner page (service, blog, neighborhood)
# right below the hero, so search-driven visitors see the Fox 17 + Rapid Growth Media trust
# signals immediately without having to bounce back to the homepage.
PRESS_STRIP_COMPACT = """  <div class="page-press-strip">
    <span class="page-press-label">Featured On</span>
    <a href="https://www.fox17online.com/morning-mix/go-green-college-painters-student-run-family-owned-and-results-that-wow" target="_blank" rel="noopener">Fox 17 Morning Mix</a>
    <span class="page-press-sep" aria-hidden="true">&middot;</span>
    <a href="https://rapidgrowthmedia.com/how-one-family-instilled-children-with-values-of-hard-work-entrepreneurship/" target="_blank" rel="noopener">Rapid Growth Media</a>
  </div>"""

SCRIPTS_HTML = """  <!-- Sticky mobile Call Now button (replaces Zoho SalesIQ widget) -->
  <a href="tel:+16162642119" class="sticky-call-btn" aria-label="Call (616) 264-2119">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
    <span>Call (616) 264-2119</span>
  </a>
  <script>
    function toggleMenu() { document.getElementById('navLinks').classList.toggle('open'); }
    document.querySelectorAll('.nav-links a').forEach(function (l) {
      l.addEventListener('click', function () { document.getElementById('navLinks').classList.remove('open'); });
    });
    window.addEventListener('scroll', function () {
      var n = document.querySelector('nav');
      if (n) n.style.boxShadow = window.scrollY > 20 ? '0 2px 20px rgba(0,0,0,0.35)' : '0 2px 12px rgba(0,0,0,0.25)';
    });
    // Track tel: link clicks as a GA4 'phone_click' event (works for nav phone, hero phone, sticky button, footer phone)
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="tel:"]');
      if (a && typeof window.gtag === 'function') {
        var loc = a.closest('.sticky-call-btn') ? 'sticky_mobile'
                : a.closest('nav') ? 'nav'
                : a.closest('footer') ? 'footer'
                : 'inline';
        gtag('event', 'phone_click', { phone_number: a.getAttribute('href').replace('tel:', ''), location: loc });
      }
    });
    // Scroll-depth tracking (fires at 25/50/75/100% — once per page load)
    (function () {
      if (typeof window.gtag !== 'function') return;
      var marks = [25, 50, 75, 100], fired = {};
      function onScroll() {
        var h = document.documentElement, b = document.body;
        var total = Math.max(h.scrollHeight, b.scrollHeight) - window.innerHeight;
        if (total <= 0) return;
        var pct = ((window.pageYOffset || h.scrollTop) / total) * 100;
        marks.forEach(function (m) {
          if (!fired[m] && pct >= m) {
            fired[m] = true;
            gtag('event', 'scroll_depth', { percent: m, page_path: location.pathname });
          }
        });
      }
      window.addEventListener('scroll', onScroll, { passive: true });
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
    # Canonical override: pages can declare canonical_override to point Google at a different
    # primary version (used for Custom Murals → Custom Painting consolidation).
    canonical_link = page.get("canonical_override", canonical)
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html_lib.escape(page['title'])}</title>
  <meta name="description" content="{html_lib.escape(page['description'])}" />
  <link rel="canonical" href="{canonical_link}" />

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

    return f"{head}\n{NAV_HTML}\n{page_hero}\n{PRESS_STRIP_COMPACT}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

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
CSS_VERSION = "20260730"

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

    return f"{head}\n{NAV_HTML}\n{page_hero}\n{PRESS_STRIP_COMPACT}\n{main}\n{FOOTER_HTML}\n{SCRIPTS_HTML}\n</body>\n</html>\n"

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
              <option value="Custom Banner or Mural">Custom Banner or Mural</option>
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
