import Link from "next/link";
import { cn } from "@/lib/utils";
import { VideoBackground } from "@/components/home/VideoBackground";

export type ResponsiveHeroBannerProps = {
  badgeLabel?: string;
  badgeText?: string;
  title?: string;
  titleLine2?: string;
  description?: string;
  primaryButtonText?: string;
  primaryButtonHref?: string;
  scrollHint?: string;
  className?: string;
};

const DEFAULTS = {
  badgeLabel: "Intelligence",
  badgeText: "Evidence-First Earth Observation",
  title: "SatQuery",
  titleLine2: "Transparency without Hallucinations.",
  description: "Advanced vision-language intelligence built for rigorous geospatial analysis.",
  primaryButtonText: "ENTER WORKSTATION",
  primaryButtonHref: "/workstation",
  scrollHint: "SCROLL TO EXPLORE",
} as const;

export function ResponsiveHeroBanner({
  badgeLabel = DEFAULTS.badgeLabel,
  badgeText = DEFAULTS.badgeText,
  title = DEFAULTS.title,
  titleLine2 = DEFAULTS.titleLine2,
  description = DEFAULTS.description,
  primaryButtonText = DEFAULTS.primaryButtonText,
  primaryButtonHref = DEFAULTS.primaryButtonHref,
  scrollHint = DEFAULTS.scrollHint,
  className,
}: ResponsiveHeroBannerProps) {
  return (
    <section
      id="home-hero"
      className={cn("responsive-hero-banner", className)}
      aria-label="SatQuery AI hero"
    >
      <VideoBackground />
      <div className="responsive-hero-banner__overlay" aria-hidden="true" />
      <div className="responsive-hero-banner__fade-bottom" aria-hidden="true" />

      <div className="responsive-hero-banner__content">
        {badgeText ? (
          <div className="responsive-hero-banner__badge bg-sat-surface border border-sat-border hero-animate hero-animate--1">
            {badgeLabel ? (
              <span className="responsive-hero-banner__badge-label">{badgeLabel}</span>
            ) : null}
            <span>{badgeText}</span>
          </div>
        ) : null}

        <h1 className="responsive-hero-banner__title hero-animate hero-animate--2">
          <span className="responsive-hero-banner__title-line">{title}</span>
        </h1>

        {titleLine2 ? (
          <p className="responsive-hero-banner__subtitle hero-animate hero-animate--3">
            {titleLine2}
          </p>
        ) : null}

        {description ? (
          <p className="responsive-hero-banner__tagline hero-animate hero-animate--4">
            {description}
          </p>
        ) : null}

        <div className="responsive-hero-banner__actions hero-animate hero-animate--5">
          <Link
            href={primaryButtonHref}
            className="responsive-hero-banner__cta"
          >
            {primaryButtonText}
          </Link>
        </div>
      </div>

      {scrollHint ? (
        <p className="responsive-hero-banner__scroll hero-animate hero-animate--6">{scrollHint}</p>
      ) : null}
    </section>
  );
}
