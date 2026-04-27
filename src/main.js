import './style.css'

/* ── Sticky Header ───────────────────────────────────────── */
const header = document.getElementById('site-header')
const logo   = document.getElementById('header-logo')

const setHeaderMode = (scrolled) => {
  if (scrolled) {
    header.classList.add('scrolled')
    // swap to dark logo once bg turns light
    logo.style.filter = 'none'
    header.querySelectorAll('.nav-link').forEach(el => {
      el.style.color = '#1A1A1A'
    })
  } else {
    header.classList.remove('scrolled')
    logo.style.filter = 'brightness(0) invert(1)'
    header.querySelectorAll('.nav-link').forEach(el => {
      el.style.color = '#ffffff'
    })
  }
}

setHeaderMode(false)
window.addEventListener('scroll', () => setHeaderMode(window.scrollY > 60), { passive: true })

/* ── Mobile Menu ─────────────────────────────────────────── */
const menuToggle = document.getElementById('menu-toggle')
const mobileMenu = document.getElementById('mobile-menu')

menuToggle.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open')
  menuToggle.setAttribute('aria-expanded', String(isOpen))
})

// Close on nav link click
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.remove('open')
    menuToggle.setAttribute('aria-expanded', 'false')
  })
})

/* ── Hero fallback ───────────────────────────────────────── */
const heroBg  = document.querySelector('#hero .hero-bg')
const heroFb  = document.getElementById('hero-fallback')
if (heroBg) {
  heroBg.addEventListener('load', () => { if (heroFb) heroFb.style.display = 'none' })
}

/* ── FAQ Accordion ───────────────────────────────────────── */
document.querySelectorAll('#faq .faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item   = btn.closest('.faq-item')
    const isOpen = item.classList.contains('open')

    // close all
    document.querySelectorAll('#faq .faq-item.open').forEach(el => {
      el.classList.remove('open')
      el.querySelector('.faq-question').setAttribute('aria-expanded', 'false')
    })

    // open clicked if it was closed
    if (!isOpen) {
      item.classList.add('open')
      btn.setAttribute('aria-expanded', 'true')
    }
  })
})

/* ── Welcome Popup ───────────────────────────────────────── */
const overlay  = document.getElementById('popup-overlay')
const closeBtn = document.getElementById('popup-close')
const dismiss  = document.getElementById('popup-dismiss')

const showPopup = () => {
  if (sessionStorage.getItem('cs-popup-shown')) return
  overlay.classList.add('visible')
  sessionStorage.setItem('cs-popup-shown', '1')
}

const hidePopup = () => overlay.classList.remove('visible')

// Trigger after 10s
setTimeout(showPopup, 10_000)

// Also on exit intent (desktop)
document.addEventListener('mouseleave', (e) => {
  if (e.clientY < 0) showPopup()
}, { once: true })

closeBtn.addEventListener('click', hidePopup)
dismiss.addEventListener('click', hidePopup)
overlay.addEventListener('click', (e) => { if (e.target === overlay) hidePopup() })

// Trap focus in popup (accessibility)
overlay.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') hidePopup()
})
