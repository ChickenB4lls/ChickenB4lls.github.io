/* ==========================================================================
   Portefeuille de points booster (partagé par toutes les pages)
   Stockage : localStorage — points + date du dernier bonus quotidien
   ========================================================================== */
(() => {
  const PTS_KEY = 'boosterPoints_v1';
  const DAILY_KEY = 'boosterDaily_v1';

  const read = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d; } catch (e) { return d; } };
  const write = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { console.warn('Sauvegarde impossible', e); } };
  const dayStr = d => d.toLocaleDateString('sv-SE'); // AAAA-MM-JJ (heure locale)

// Récompense fixe de 75 points par jour
const rewardFor = () => 75;

const Wallet = {
  COST: 10,
  rewardFor,
  get: () => Math.max(0, Math.floor(Number(read(PTS_KEY, 0)) || 0)),
  set(n) { write(PTS_KEY, Math.max(0, Math.floor(n))); notify(); },
  add(n) { this.set(this.get() + n); },
  spend(n) {
    if (this.get() < n) return false;
    this.set(this.get() - n);
    return true;
  },
  // État du bonus quotidien fixe
  daily() {
    const d = read(DAILY_KEY, { last: null });
    const today = dayStr(new Date());
    const claimed = d.last === today;
    return { claimed, reward: 75 };
  },
  // Réclame les 75 points du jour
  claim() {
    const s = this.daily();
    if (s.claimed) return null;
    write(DAILY_KEY, { last: dayStr(new Date()) });
    this.add(75);
    return { reward: 75 };
  }
};

  function notify() {
    document.querySelectorAll('[data-pts]').forEach(el => { el.textContent = Wallet.get(); });
    window.dispatchEvent(new CustomEvent('wallet'));
  }

  /* --- Fichier: shared.js --- */
function buildHud() {
  const page = document.body.dataset.hud;
  if (!page) return;

  // Remplacement de l'émoji par la balise <img> pour les boosters
  const links = [
    ['index.html', 'Accueil', 'home'],
    ['boosters.html', 'Boosters', 'boosters'],
    ['casino.html', 'Casino', 'casino']
  ].filter(l => page !== 'home' && l[2] !== page);

  const hud = document.createElement('div');
  hud.className = 'hud';
  hud.innerHTML = links.map(l => `<a href="${l[0]}" aria-label="${l[1]}"><span>${l[1]}</span></a>`).join('')
    + '<div class="pts"><span data-pts>0</span> pts</div>';
    
  document.body.appendChild(hud);
}

  window.Wallet = Wallet;
  window.addEventListener('storage', notify); // synchro entre onglets
  document.addEventListener('DOMContentLoaded', () => { buildHud(); notify(); });
})();
