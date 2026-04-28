# CSS Design Patterns for Slide Presentations

## Base Setup

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

```css
:root {
  /* Primary palette (Serendie-inspired) */
  --primary: #174ECC;
  --primary-dark: #0B2D7A;
  --primary-50: #EEF3FF;
  --primary-100: #DCE7FF;
  --accent: #8A42FF;
  --accent-50: #F3ECFF;
  --success: #12A07F;
  --success-50: #E0F6EF;
  --warn: #E8820C;
  --warn-50: #FFF4E3;
  --danger: #E0364A;

  /* Text */
  --ink: #0F1629;
  --ink-soft: #1F2A44;
  --muted: #5F6B7A;

  /* Surfaces */
  --line: #E3E8F0;
  --bg: #FFFFFF;
  --bg-soft: #F5F7FB;
  --bg-mist: #FAFBFE;
  --radius: 18px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #24324a; font-family: "Noto Sans JP", "Yu Gothic UI", sans-serif; }
body { padding: 40px 0; display: flex; flex-direction: column; align-items: center; gap: 32px; }

.slide {
  width: 1920px; height: 1080px; background: var(--bg);
  position: relative; overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,.25);
}
```

## Slide Shell Structure

Every content slide should follow this shell:

```html
<section class="slide" id="sN">
  <!-- Header (optional) -->
  <div class="header">
    <div class="title-wrap">
      <div class="bar"></div>
      <div>
        <div class="t">スライドタイトル</div>
        <div class="st">サブタイトル</div>
      </div>
    </div>
    <div class="logo"><div class="dot"></div>APP NAME</div>
  </div>
  <!-- Main content area -->
  <div class="content">
    <!-- slide body here -->
  </div>
  <!-- Footer elements -->
  <div class="brandline"><span class="bl-dot"></span>AppName</div>
  <div class="pager">N / TOTAL</div>
</section>
```

```css
.header {
  position: absolute; top: 56px; left: 80px; right: 80px;
  display: flex; align-items: flex-end; justify-content: space-between;
  padding-bottom: 28px; border-bottom: 1px solid var(--line);
}
.header .bar { width: 8px; height: 56px; background: var(--primary); border-radius: 4px; }
.header .t { font-size: 42px; font-weight: 800; color: var(--ink); }
.header .st { font-size: 18px; color: var(--muted); font-weight: 500; margin-top: 8px; }
.header .logo { display: flex; align-items: center; gap: 10px; color: var(--muted); font-size: 14px; font-weight: 700; }
.header .logo .dot { width: 10px; height: 10px; background: var(--primary); border-radius: 50%; }

.pager { position: absolute; bottom: 48px; right: 80px; font-size: 16px; color: var(--muted); font-weight: 700; }
.brandline { position: absolute; bottom: 48px; left: 80px; display: flex; align-items: center; gap: 14px; font-size: 14px; color: var(--muted); font-weight: 700; }
.brandline .bl-dot { width: 8px; height: 8px; background: var(--primary); border-radius: 50%; }

.content { position: absolute; top: 200px; left: 80px; right: 80px; bottom: 120px; }
```

## Slide Type Patterns

### Cover Slide

```css
#s1 {
  background: radial-gradient(ellipse at 10% 20%, #2E6DE8, transparent 55%),
              radial-gradient(ellipse at 90% 90%, #8A42FF, transparent 55%),
              linear-gradient(135deg, #0B2D7A, #174ECC 60%, #2E75FF);
  color: #fff;
}
.cover-wrap {
  position: absolute; inset: 0; padding: 120px;
  display: flex; flex-direction: column; justify-content: space-between; z-index: 2;
}
.main-ttl { font-size: 120px; font-weight: 900; line-height: .96; letter-spacing: -.03em; }
.sub-ttl { font-size: 32px; font-weight: 500; opacity: .92; margin-top: 28px; line-height: 1.55; }
/* Frosted chip row */
.chips { display: flex; gap: 14px; margin-top: 32px; }
.chip { background: rgba(255,255,255,.14); backdrop-filter: blur(8px); padding: 12px 22px; border-radius: 999px; font-size: 17px; font-weight: 700; border: 1px solid rgba(255,255,255,.25); }
```

### Chapter / Section Divider

```css
.ch-wrap { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 0 140px; }
.ch-kicker { font-size: 22px; font-weight: 800; letter-spacing: .2em; color: var(--primary); margin-bottom: 28px; }
.ch-title { font-size: 120px; font-weight: 900; line-height: 1.02; letter-spacing: -.02em; color: var(--ink); }
.ch-sub { font-size: 30px; color: var(--muted); font-weight: 500; margin-top: 32px; line-height: 1.6; max-width: 1400px; }
/* Decorative radial glow in top-right */
.ch-deco { position: absolute; right: -160px; top: -160px; width: 900px; height: 900px; background: radial-gradient(circle, var(--primary-50), transparent 65%); z-index: 0; }
/* AI variant: dark purple */
.ch-ai { background: linear-gradient(135deg, #140B3A 0%, #3A1E8F 55%, #8A42FF 100%); color: #fff; }
```

### Feature Layout (Text Left / Screenshot Right)

```css
.ft-layout { display: grid; grid-template-columns: 1fr 1.55fr; gap: 48px; height: 100%; }
.ft-left { display: flex; flex-direction: column; gap: 22px; }
```

### Two-Column Card Grid

```css
.two-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; }
.two-cards .card-box { background: var(--bg-mist); border: 1px solid var(--line); border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 16px; }
.two-cards .card-box .ttl { font-size: 28px; font-weight: 800; color: var(--ink); }
```

### Big Statement / One-liner

```css
.one-liner { display: flex; flex-direction: column; gap: 20px; align-items: center; justify-content: center; height: 100%; text-align: center; }
.one-liner .kicker { font-size: 22px; font-weight: 800; letter-spacing: .12em; color: var(--primary); }
.one-liner .big { font-size: 92px; font-weight: 900; line-height: 1.15; letter-spacing: -.02em; }
```

### Bullet List

```css
.blist { display: flex; flex-direction: column; gap: 18px; }
.blist .bi { display: flex; gap: 16px; font-size: 20px; color: var(--ink-soft); line-height: 1.6; }
.blist .bi::before { content: ""; width: 8px; height: 8px; background: var(--primary); border-radius: 50%; flex-shrink: 0; margin-top: 14px; }
.blist.accent .bi::before { background: var(--accent); }
```

### Step / Progress Indicators

```css
/* Numbered pill button */
.step-pill {
  display: inline-flex; align-items: center; gap: 14px;
  padding: 10px 16px 10px 10px; background: var(--primary); color: #fff;
  border-radius: 999px; font-weight: 800; font-size: 18px;
}
.step-pill .num { background: #fff; color: var(--primary); border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; }

/* Progress bar (journey-style) */
.jn-progress { position: absolute; top: 170px; left: 80px; right: 80px; display: flex; align-items: center; gap: 10px; }
.jn-progress .pstep { display: flex; align-items: center; gap: 10px; padding: 8px 14px; border-radius: 999px; background: var(--bg-mist); border: 1px solid var(--line); font-size: 13px; font-weight: 700; color: var(--muted); }
.jn-progress .pstep.active { background: var(--primary); color: #fff; }
.jn-progress .pstep.done { background: var(--success-50); color: var(--success); border-color: #C3EADD; }
.jn-progress .pline { flex: 1; height: 2px; background: var(--line); }
```

### Screenshot Frame

```css
.shot {
  border-radius: 14px; overflow: hidden; background: #fff;
  box-shadow: 0 30px 70px -25px rgba(15,22,41,.4), 0 6px 20px -4px rgba(15,22,41,.1);
  border: 1px solid var(--line);
}
.shot img { display: block; width: 100%; height: auto; }
```

### AI Badge / Tag Chips

```css
.ai-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #8A42FF, #B072FF);
  color: #fff; font-weight: 800; font-size: 16px; padding: 10px 18px; border-radius: 999px;
  box-shadow: 0 6px 20px rgba(138,66,255,.35);
}
.tag { display: inline-block; padding: 6px 14px; border-radius: 999px; font-size: 14px; font-weight: 800; letter-spacing: .08em; }
.tag.primary { background: var(--primary-50); color: var(--primary); }
.tag.accent { background: var(--accent-50); color: var(--accent); }
.tag.success { background: var(--success-50); color: var(--success); }
```

### Callout / Info Box

```css
.callout {
  display: flex; align-items: center; gap: 16px; padding: 20px 28px;
  background: linear-gradient(90deg, var(--primary-50), #fff);
  border-left: 5px solid var(--primary); border-radius: 14px;
  font-size: 20px; color: var(--ink-soft); font-weight: 700;
}
```

### Thank You / Closing Slide

> **重要**: 最終スライドも `#sN`（連番）で命名すること。レンダラーは `#s1`〜`#sN` を順番に処理するため、`#sLAST` のような名前はスクリーンショットされない。

```css
/* 例: 14枚構成なら #s14 に適用 */
#s14 {
  background: linear-gradient(135deg, #0B2D7A, #174ECC 55%, #2E75FF);
  color: #fff; position: relative; overflow: hidden;
}
#s14::before { content: ""; position: absolute; top: -200px; left: -100px; width: 700px; height: 700px; background: radial-gradient(circle, rgba(255,255,255,.18), transparent 60%); }
#s14::after  { content: ""; position: absolute; bottom: -200px; right: -100px; width: 600px; height: 600px; background: radial-gradient(circle, rgba(138,66,255,.4), transparent 60%); }
.ty-wrap { position: relative; z-index: 2; padding: 140px 120px; height: 100%; display: flex; flex-direction: column; justify-content: center; gap: 36px; }
.ty-big { font-size: 200px; font-weight: 900; line-height: .96; letter-spacing: -.03em; }
```

## Highlighted Text Inline

```css
.hl    { background: linear-gradient(180deg, transparent 60%, #FFE788 60%); padding: 0 4px; } /* yellow */
.hl-ai { background: linear-gradient(180deg, transparent 60%, #E4D2FF 60%); padding: 0 4px; } /* purple */
```

## Gradient Text

```css
.gradient-text {
  background: linear-gradient(135deg, #8A42FF, #174ECC);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
```
