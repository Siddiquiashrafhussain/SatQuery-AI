import Link from "next/link";
import Image from "next/image";

export function HomeFooter() {
  return (
    <footer className="home-footer">
      <div className="home-footer__inner">
        <div className="home-footer__columns">
          <div className="home-footer__column">
            <p className="home-footer__heading">Product</p>
            <ul className="home-footer__links">
              <li>
                <Link href="/workstation">Workstation</Link>
              </li>
              <li>
                <Link href="/tutorial">Tutorial</Link>
              </li>
              <li>
                <Link href="#about">About</Link>
              </li>
            </ul>
          </div>

          <div className="home-footer__column home-footer__column--about">
            <Link href="/" className="mb-4 block">
              <Image src="/LOGO.png" alt="SatQuery AI" width={160} height={41} className="brightness-200 contrast-125" />
            </Link>
            <p className="home-footer__about text-sm">
              SatQuery AI — a functional prototype for interactive Earth observation intelligence.
            </p>
          </div>
        </div>

        <div className="home-footer__bar">
          <p className="home-footer__copy">© 2026 SatQuery AI</p>
        </div>
      </div>
    </footer>
  );
}
