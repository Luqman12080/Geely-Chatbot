import React, { useMemo, useState } from "react";
import "./styles/landing.css";
import Porsche from "../assets/Porsche.jpg";
import BMW from "../assets/BMW.jpg";
import GT3 from "../assets/gt3.jpg";

const VEHICLES = [
  {
    make: "Porsche",
    model: "911 Carrera GTS",
    year: 2026,
    price: "164,500",
    miles: "12 mi",
    fuel: "Gasoline",
    drive: "AWD",
    tag: "NEW",
    tagClass: "new",
    cat: ["new", "coupe"],
    image: Porsche,
  },
  {
    make: "Porsche",
    model: "911 GT3",
    year: 2026,
    price: "198,400",
    miles: "24 mi",
    fuel: "Gasoline",
    drive: "AWD",
    tag: "NEW",
    tagClass: "new",
    cat: ["new", "coupe"],
    image: GT3,
  },
  {
    make: "BMW M",
    model: "i7 M70 xDrive",
    year: 2025,
    price: "168,300",
    miles: "4,210 mi",
    fuel: "Electric",
    drive: "AWD",
    tag: "CPO",
    tagClass: "cpo",
    cat: ["cpo", "sedan", "ev"],
    image: BMW,
  },
];

const FILTERS = [
  { key: "all", label: "All", count: 412 },
  { key: "new", label: "New", count: 186 },
  { key: "cpo", label: "Certified Pre-Owned", count: 142 },
  { key: "suv", label: "SUV", count: 98 },
  { key: "sedan", label: "Sedan", count: 124 },
  { key: "coupe", label: "Coupe / GT", count: 62 },
  { key: "ev", label: "Electric", count: 88 },
];

function tryOpenChatWidget() {
  const chatBtn = document.querySelector(".chatbot-container .chat-button");
  if (chatBtn) chatBtn.click();
}

function BrandMark({ variant = "dark" }) {
  const stroke = variant === "dark" ? "#30333f" : "#fff";
  const circle = variant === "dark" ? "#30333f" : "#fff";
  return (
    <svg viewBox="0 0 28 28" fill="none" aria-hidden="true">
      <rect x="2" y="2" width="24" height="24" stroke={stroke} strokeWidth="1.5" />
      <path d="M8 14 L14 8 L20 14 L14 20 Z" fill="#28a9e0" />
      <circle cx="14" cy="14" r="2" fill={circle} />
    </svg>
  );
}

function VehicleCard({ v, isFav, onToggleFav }) {
  return (
    <article className="csm-vehicle">
      <div className="csm-vehicle-img">
        <span className={`csm-vehicle-tag ${v.tagClass}`}>{v.tag}</span>
        <button
          className={`csm-vehicle-fav ${isFav ? "active" : ""}`}
          onClick={onToggleFav}
          type="button"
          aria-label="Save"
        >
          <svg viewBox="0 0 24 24">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
        </button>
        {v.image ? (
          <img className="csm-vehicle-photo" src={v.image} alt={`${v.year} ${v.make} ${v.model}`} loading="lazy" />
        ) : (
          <div className="csm-placeholder light">
            <div className="csm-placeholder-tag">{v.make.toUpperCase()} · VEHICLE PHOTO</div>
          </div>
        )}
      </div>

      <div className="csm-vehicle-body">
        <div className="csm-vehicle-row">
          <div className="csm-vehicle-make">{v.make}</div>
          <div className="csm-vehicle-year">{v.year}</div>
        </div>

        <div className="csm-vehicle-name">{v.model}</div>

        <div className="csm-vehicle-meta">
          <span>
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
            {v.miles}
          </span>
          <span>
            <svg viewBox="0 0 24 24">
              <path d="M3 7l9-4 9 4v10l-9 4-9-4z" />
              <path d="M3 7l9 4 9-4M12 11v10" />
            </svg>
            {v.fuel}
          </span>
          <span>
            <svg viewBox="0 0 24 24">
              <circle cx="6" cy="18" r="3" />
              <circle cx="18" cy="6" r="3" />
              <path d="M9 18h9M6 15V9a3 3 0 0 1 3-3h6" />
            </svg>
            {v.drive}
          </span>
        </div>

        <div className="csm-vehicle-foot">
          <div className="csm-vehicle-price">
            <span className="pre">USD</span>${v.price}
          </div>
          <div className="csm-vehicle-cta">
            View Details
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </div>
        </div>
      </div>
    </article>
  );
}

export default function LandingPage() {
  const [filter, setFilter] = useState("all");
  const [fav, setFav] = useState(() => new Set());

  const list = useMemo(() => {
    if (filter === "all") return VEHICLES;
    return VEHICLES.filter((v) => v.cat.includes(filter));
  }, [filter]);

  const featured = VEHICLES[0];

  return (
    <div className="csm-shell">
      <nav className="csm-nav">
        <div className="csm-nav-inner">
          <a href="#top" className="csm-brand" aria-label="Cinergie Digital Motors">
            <div className="csm-brand-mark">
              <BrandMark variant="dark" />
            </div>
            <div className="csm-brand-name">
              CINERGIE <span>DIGITAL MOTORS</span>
            </div>
          </a>

          <div className="csm-nav-links">
            <a href="#inventory">Inventory</a>
            <a href="#new">New</a>
            <a href="#preowned">Pre-Owned</a>
            <a href="#finance">Finance</a>
            <a href="#service">Service</a>
            <a href="#about">About</a>
          </div>

          <div className="csm-nav-cta">
            <a href="tel:+18005551234" className="phone">
              +1 (800) 555-1234
            </a>
            <button className="csm-btn" type="button">
              Schedule Test Drive
            </button>
          </div>
        </div>
      </nav>

      <section className="csm-hero" id="top">
        <div className="csm-hero-grid">
          <div className="csm-hero-text">
            <div className="csm-hero-eyebrow">SPRING COLLECTION · 2026</div>
            <h1>
              The road, <em>reimagined</em>.
            </h1>
            <p className="csm-hero-sub">
              Curated luxury and performance vehicles, delivered with the most intelligent dealership experience on the web. Browse,
              configure, and finance — all in one conversation.
            </p>

            <div className="csm-hero-actions">
              <a className="csm-btn csm-btn-light" href="#inventory">
                Browse Inventory
              </a>
              <button className="csm-btn csm-btn-hero-ghost" type="button" onClick={tryOpenChatWidget}>
                Talk to Cinergie AI →
              </button>
            </div>

            <div className="csm-hero-stats">
              <div>
                <div className="csm-stat-num">412</div>
                <div className="csm-stat-label">Vehicles in stock</div>
              </div>
              <div>
                <div className="csm-stat-num">38</div>
                <div className="csm-stat-label">Premium brands</div>
              </div>
              <div>
                <div className="csm-stat-num">24/7</div>
                <div className="csm-stat-label">AI Concierge</div>
              </div>
            </div>
          </div>

          <div className="csm-hero-image" aria-hidden="true">
            {featured?.image ? (
              <img className="csm-hero-photo" src={featured.image} alt="" />
            ) : (
              <div className="csm-placeholder">
                <div className="csm-placeholder-tag">Hero Vehicle Photo · 4:5</div>
              </div>
            )}
            <div className="csm-hero-image-meta">
              <div>
                <div className="csm-hero-image-kicker">FEATURED</div>
                <div className="csm-hero-image-title">
                  {featured ? `${featured.year} ${featured.make} ${featured.model}` : "Featured Vehicle"}
                </div>
              </div>
              <div className="csm-hero-image-price">{featured ? `$${featured.price}` : ""}</div>
            </div>
          </div>
        </div>
      </section>

      <div className="csm-brand-bar" aria-label="Brands">
        <div className="csm-brand-bar-inner">
          <span>Aston Martin</span>
          <span>Bentley</span>
          <span>Porsche</span>
          <span>Maserati</span>
          <span>Mercedes-AMG</span>
          <span>Lexus</span>
          <span>Range Rover</span>
          <span>BMW M</span>
        </div>
      </div>

      <section className="csm-section" id="inventory">
        <div className="csm-section-head">
          <div className="csm-section-head-l">
            <div className="csm-section-eyebrow">FEATURED INVENTORY</div>
            <h2 className="csm-section-title">
              Hand-picked, <em>showroom-ready</em>.
            </h2>
          </div>
          <p className="csm-section-desc">
            Every vehicle in our collection is inspected, certified, and prepared by master technicians — and ready for delivery within 48
            hours.
          </p>
        </div>

        <div className="csm-filters" role="tablist" aria-label="Inventory filters">
          {FILTERS.map((f) => (
            <button
              key={f.key}
              className={`csm-filter ${filter === f.key ? "active" : ""}`}
              type="button"
              onClick={() => setFilter(f.key)}
            >
              {f.label} <span className="count">{f.count}</span>
            </button>
          ))}
        </div>

        <div className="csm-vehicles">
          {list.map((v) => {
            const id = `${v.make}-${v.model}-${v.year}`;
            const isFav = fav.has(id);
            return (
              <VehicleCard
                key={id}
                v={v}
                isFav={isFav}
                onToggleFav={() => {
                  setFav((prev) => {
                    const next = new Set(prev);
                    if (next.has(id)) next.delete(id);
                    else next.add(id);
                    return next;
                  });
                }}
              />
            );
          })}
        </div>

        <div className="csm-grid-foot">
          <button className="csm-btn csm-btn-ghost" type="button">
            View Full Inventory →
          </button>
        </div>
      </section>

      <footer className="csm-footer">
        <div className="csm-foot-inner">
          <div className="csm-foot-top">
            <div className="csm-foot-brand-block">
              <a href="#top" className="csm-brand">
                <div className="csm-brand-mark">
                  <BrandMark variant="light" />
                </div>
                <div className="csm-brand-name">
                  CINERGIE <span>DIGITAL MOTORS</span>
                </div>
              </a>

              <div className="csm-foot-tag">
                Premium vehicles, <em>intelligently</em> matched.
              </div>

              <div className="csm-foot-address">
                1280 Innovation Boulevard
                <br />
                Suite 400
                <br />
                Detroit, MI 48201
                <br />
                <br />
                Mon–Sat · 9:00 AM – 8:00 PM
                <br />
                Sun · 11:00 AM – 6:00 PM
              </div>
            </div>

            <div className="csm-foot-col">
              <h4>Inventory</h4>
              <ul>
                <li>
                  <a href="#inventory">New Vehicles</a>
                </li>
                <li>
                  <a href="#inventory">Pre-Owned</a>
                </li>
                <li>
                  <a href="#inventory">Certified Pre-Owned</a>
                </li>
                <li>
                  <a href="#inventory">Electric & Hybrid</a>
                </li>
                <li>
                  <a href="#inventory">Coupes & GTs</a>
                </li>
                <li>
                  <a href="#inventory">Specialty</a>
                </li>
              </ul>
            </div>

            <div className="csm-foot-col">
              <h4>Services</h4>
              <ul>
                <li>
                  <a href="#finance">Financing</a>
                </li>
                <li>
                  <a href="#service">Trade-In</a>
                </li>
                <li>
                  <a href="#service">Service Center</a>
                </li>
                <li>
                  <a href="#service">Parts</a>
                </li>
                <li>
                  <a href="#service">Concierge Delivery</a>
                </li>
                <li>
                  <a href="#service">Warranty</a>
                </li>
              </ul>
            </div>

            <div className="csm-foot-col">
              <h4>Company</h4>
              <ul>
                <li>
                  <a href="#about">About</a>
                </li>
                <li>
                  <button className="csm-linklike" type="button" onClick={tryOpenChatWidget}>
                    The Cinergie AI
                  </button>
                </li>
                <li>
                  <a href="#about">Press</a>
                </li>
                <li>
                  <a href="#about">Careers</a>
                </li>
                <li>
                  <a href="#about">Contact</a>
                </li>
                <li>
                  <a href="#about">Visit Showroom</a>
                </li>
              </ul>
            </div>

            <div className="csm-foot-col csm-newsletter">
              <h4>Stay in the loop</h4>
              <p>Be the first to see new arrivals, allocations, and members-only offers.</p>
              <input type="email" placeholder="your@email.com" />
              <button className="csm-btn csm-btn-light csm-full" type="button">
                Subscribe
              </button>
            </div>
          </div>

          <div className="csm-foot-bottom">
            <div>© 2026 Cinergie Digital Motors. All rights reserved.</div>
            <div className="csm-foot-bottom-links">
              <a href="#top">Privacy</a>
              <a href="#top">Terms</a>
              <a href="#top">Accessibility</a>
              <a href="#top">Sitemap</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

