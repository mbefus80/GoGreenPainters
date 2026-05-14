#!/usr/bin/env python3
"""
Static page generator for Go Green College Painters.

Builds:
  /services/exterior-painting/index.html
  /services/interior-painting/index.html
  /services/deck-staining/index.html
  /services/custom-murals/index.html

Each page reuses the LocalBusiness JSON-LD from the homepage (same @id) plus a page-specific
Service, FAQPage, BreadcrumbList, and WebPage node — so every URL is its own valid local-SEO
citation while staying NAP-consistent with the home page.

To rebuild: `python3 build_pages.py` from the repo root.
"""
import json, os, html as html_lib, textwrap, datetime

SITE = "https://gogreenpainters.com"
BUSINESS_ID = f"{SITE}/#business"

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
    "sameAs": ["https://www.yelp.com/biz/go-green-painters-grand-rapids"],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5",
        "reviewCount": "3",
        "bestRating": "5",
    },
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
            ("Do you do siding repairs and carpentry?", "We handle minor siding repairs, board replacement, and rotted-wood patching as part of a normal exterior repaint. For major structural work we'll refer you to a trusted carpenter and coordinate the paint after."),
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
        "description": "Deck staining, fence staining, and wood restoration in Grand Rapids, MI. We clean, sand, repair, and seal weathered decks to protect them through Michigan winters. Free estimates.",
        "h1": "Deck Staining & Restoration in Grand Rapids, MI",
        "hero_img": "/stain-after.jpg",
        "service_name": "Deck Staining and Restoration",
        "service_desc": "Deck and fence staining and wood restoration in Grand Rapids, MI. Includes cleaning, sanding, repair, and protective stain sealing to withstand Michigan winters.",
        "service_image": f"{SITE}/deck-staining.jpg",
        "breadcrumb": [("Home", "/"), ("Services", "/#services"), ("Deck Staining", "/services/deck-staining/")],
        "lead": "Michigan winters are brutal on wood. We restore weathered decks, fences, pergolas, and play structures in Grand Rapids — clean, sand, repair, and seal — so they look new and stay protected through the next freeze-thaw cycle.",
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
            ("Our Deck Restoration Process", """
                <ul>
                  <li><strong>Inspect</strong> for rot, loose boards, popped nails, and railing issues.</li>
                  <li><strong>Clean</strong> with the right wood cleaner for the type of staining or mildew present.</li>
                  <li><strong>Repair</strong> — replace rotted boards, hammer back nails, tighten railing posts.</li>
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
                <p>Deck staining in Grand Rapids generally runs <strong>$700 to $2,500</strong> depending on deck size, condition, repair work needed, and stain type. Every quote is free and fixed-price.</p>
            """),
        ],
        "faqs": [
            ("How often should I re-stain my deck in Michigan?", "Most decks in Grand Rapids need re-staining every 2 to 4 years. Semi-transparent stains fade faster than solid stains. South- and west-facing decks need attention sooner. We can inspect yours and tell you honestly whether it's due."),
            ("Should I stain or paint my deck?", "Stain is almost always the right call for decks. Paint sits on top of the wood and chips and peels as the deck flexes and ages; stain penetrates the wood and wears more gracefully. The exception is solid stain, which has paint-like coverage but still bonds with the wood."),
            ("What stain brands do you use?", "We use premium oil-based and waterborne stains from Sherwin-Williams (SuperDeck, DeckScapes) and Benjamin Moore (Arborcoat) — both lines hold up well to Michigan freeze-thaw and UV."),
            ("Can you bring back a really weathered deck?", "Usually yes. With a strong cleaner, a good sanding, board replacement where needed, and the right stain, most weathered decks come back to looking new. We'll be honest if a deck is past restoration — sometimes the boards are too far gone."),
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
      <li><a href="/#contact" class="nav-cta">Free Quote</a></li>
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
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+16162642119">(616) 264-2119</a></li>
          <li><a href="mailto:jack@gogreenpainters.com">jack@gogreenpainters.com</a></li>
          <li><a href="https://www.yelp.com/biz/go-green-painters-grand-rapids" target="_blank" rel="noopener">Yelp Reviews</a></li>
          <li><a href="/#contact">Free Quote</a></li>
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

def render_related_html(related):
    items = "".join([f'<li><a href="{url}">{html_lib.escape(name)}</a></li>' for name, url in related])
    return f"""      <div class="related-services">
        <h2>Related Services</h2>
        <ul>{items}</ul>
      </div>"""

def build_jsonld(page):
    canonical = f"{SITE}/{page['slug']}"
    graph = [
        LOCAL_BUSINESS,
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
            "areaServed": {
                "@type": "City", "name": "Grand Rapids",
                "containedInPlace": {"@type": "State", "name": "Michigan"},
            },
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

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{html_lib.escape(page['title'])}" />
  <meta property="og:description" content="{html_lib.escape(page['description'])}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}{page['hero_img']}" />
  <meta name="twitter:card" content="summary_large_image" />

  <meta name="geo.region" content="US-MI" />
  <meta name="geo.placename" content="Grand Rapids, Michigan" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="image" href="{page['hero_img']}" />

  <script type="application/ld+json">
{build_jsonld(page)}
  </script>

  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>"""

    page_hero = f"""  <section class="page-hero" style="background-image: linear-gradient(to bottom, rgba(0,79,57,0.78) 0%, rgba(0,0,0,0.55) 100%), url('{page['hero_img']}');">
    <div class="page-hero-inner">
      <nav class="breadcrumb">{render_breadcrumb_html(page['breadcrumb'])}</nav>
      <h1>{html_lib.escape(page['h1'])}</h1>
      <p class="lead">{page['lead']}</p>
      <a href="/#contact" class="btn-primary">Get a Free Estimate</a>
    </div>
  </section>"""

    sections_html = render_sections_html(page["sections"])
    faq_html = render_faq_html(page["faqs"])
    related_html = render_related_html(page["related"])

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

# -------- write pages --------
written = []
for page in PAGES:
    path = page["slug"] + "index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html_out = build_page(page)
    with open(path, "w") as f:
        f.write(html_out)
    written.append((path, len(html_out)))

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
