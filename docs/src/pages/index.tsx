import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function PuzzleHero() {
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className={styles.logoSection}>
          <img 
            src="/puzzle/img/logo.png" 
            alt="PUZZLE Logo" 
            className={styles.heroLogo}
          />
          <Heading as="h1" className={clsx(styles.heroTitle, 'glitch-text')}>
            PUZZLE
          </Heading>
        </div>
        
        <p className={styles.heroSlogan}>
          SELF-HOSTED ASSET MANAGEMENT WITHOUT THIRD PARTIES
        </p>
        
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            GET STARTED
          </Link>
          <Link
            className="button button--outline button--secondary button--lg"
            to="/docs/getting-started/installation">
            INSTALLATION
          </Link>
        </div>
        
        <div className={styles.terminalPrompt}>
          <span className={styles.promptSymbol}>$</span>
          <span className={styles.promptText}>
            sudo ./puzzle <span className={styles.animatedCommand}></span>
          </span>
          <span className={styles.cursor}>_</span>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="PUZZLE - Self-Hosted Asset Management"
      description="Manage your assets without relying on third parties to host 
        your data and frontend. Complete control over your financial data.">
      <PuzzleHero />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
