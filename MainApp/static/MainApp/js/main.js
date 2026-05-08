/* ============================================================
   PORTFOLIO — MAIN JAVASCRIPT
   ============================================================ */

/* ---------- 1. THEME TOGGLE ---------- */
(function () {
  var btn = document.getElementById('themeBtn');
  if (!btn) return;

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  btn.addEventListener('click', function () {
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    applyTheme(current === 'light' ? 'dark' : 'light');
  });
})();

/* ---------- 2. NAVBAR — SCROLL BEHAVIOUR & ACTIVE LINK ---------- */
(function () {
  var navbar = document.getElementById('navbar');
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');

  // Scroll shadow
  window.addEventListener('scroll', function () {
    if (navbar) {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }
  }, { passive: true });

  // Mobile menu
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      var isOpen = navLinks.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
    });

    // Close on link click
    navLinks.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target) && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Active nav link based on current path
  var path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-link[data-page]').forEach(function (link) {
    var href = link.getAttribute('href').replace(/\/$/, '') || '/';
    if (path === href || (path.startsWith(href) && href !== '/')) {
      link.classList.add('active');
    }
  });
})();

/* ---------- 3. SCROLL REVEAL ANIMATIONS ---------- */
(function () {
  var elements = document.querySelectorAll('.reveal');
  if (!elements.length) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  elements.forEach(function (el) { observer.observe(el); });
})();

/* ---------- 4. FLASH MESSAGE AUTO-DISMISS ---------- */
(function () {
  var msgs = document.querySelectorAll('.flash');
  msgs.forEach(function (msg) {
    setTimeout(function () {
      msg.style.opacity = '0';
      msg.style.transition = 'opacity .4s ease';
      setTimeout(function () { msg.remove(); }, 400);
    }, 6000);
  });
})();

/* ---------- 5. CHATBOT ---------- */
(function () {
  var fab      = document.getElementById('chatbotFab');
  var win      = document.getElementById('chatbotWindow');
  var closeBtn = document.getElementById('chatbotClose');
  var body_    = document.getElementById('chatbotBody');
  var input    = document.getElementById('chatInput');
  var sendBtn  = document.getElementById('chatSend');
  var badge    = document.getElementById('fabBadge');
  var fabOpen  = fab ? fab.querySelector('.fab-open')  : null;
  var fabClose = fab ? fab.querySelector('.fab-close') : null;

  if (!fab || !win || !body_ || !input || !sendBtn) return;

  var isOpen    = false;
  var isBusy    = false;
  var isAnimating = false;
  var CLOSE_MS  = 260;
  var conversationHistory = [];   // [{role:'user'|'bot', text:'...'}]

  /* ── Open ─────────────────────────────────────────────────── */
  function openChat() {
    isOpen      = true;
    isAnimating = true;

    win.style.display = 'flex';
    win.classList.remove('closing');
    // Force animation replay every open
    win.style.animation = 'none';
    void win.offsetWidth;
    win.style.animation = '';

    if (fabOpen)  fabOpen.style.display  = 'none';
    if (fabClose) fabClose.style.display = 'block';
    if (badge)    badge.style.display    = 'none';

    fab.style.animationPlayState = 'paused';
    fab.setAttribute('aria-label', 'Close chat with Dee');

    setTimeout(function () { isAnimating = false; }, CLOSE_MS);
    setTimeout(function () { input.focus(); }, 120);
  }

  /* ── Close ────────────────────────────────────────────────── */
  function closeChat() {
    if (!isOpen || isAnimating) return;
    isOpen      = false;
    isAnimating = true;

    win.classList.add('closing');

    if (fabOpen)  fabOpen.style.display  = 'block';
    if (fabClose) fabClose.style.display = 'none';

    fab.style.animationPlayState = 'running';
    fab.setAttribute('aria-label', 'Open chat with Dee');

    setTimeout(function () {
      win.style.display = 'none';
      win.classList.remove('closing');
      isAnimating = false;
    }, CLOSE_MS);
  }

  /* Single authoritative toggle — stopPropagation prevents bubbling */
  fab.addEventListener('click', function (e) {
    e.stopPropagation();
    if (isAnimating) return;
    isOpen ? closeChat() : openChat();
  });
  if (closeBtn) closeBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    closeChat();
  });

  /* ── DOM helpers ──────────────────────────────────────────── */
  function renderMarkdown(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  }

  function addMsg(text, who) {
    var wrap   = document.createElement('div');
    wrap.className = 'chat-msg ' + who;
    var bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    if (who === 'bot') {
      bubble.innerHTML = renderMarkdown(text);
    } else {
      bubble.textContent = text;
    }
    wrap.appendChild(bubble);
    body_.appendChild(wrap);
    body_.scrollTop = body_.scrollHeight;
    return wrap;
  }

  function showTyping() {
    var wrap = document.createElement('div');
    wrap.className = 'chat-msg bot';
    wrap.id = 'typingIndicator';
    wrap.innerHTML =
      '<div class="msg-bubble">' +
        '<div class="typing-indicator">' +
          '<div class="typing-dot"></div>' +
          '<div class="typing-dot"></div>' +
          '<div class="typing-dot"></div>' +
        '</div>' +
      '</div>';
    body_.appendChild(wrap);
    body_.scrollTop = body_.scrollHeight;
  }

  function removeTyping() {
    var t = document.getElementById('typingIndicator');
    if (t) t.remove();
  }

  function setLocked(locked) {
    isBusy           = locked;
    sendBtn.disabled = locked;
    input.disabled   = locked;
    if (!locked) input.focus();
  }

  /* ── Local keyword engine (fallback & instant response) ───── */
  var KB = [
    {
      keys: ['hello','hi','hey','good morning','good afternoon','howdy','sup','hiya'],
      reply: "Hi there! I'm Dee 👋 — your AI guide to this portfolio. Ask me about projects, skills, experience, or how to get in touch!"
    },
    {
      keys: ['bye','goodbye','see you','take care','later','ciao','farewell'],
      reply: "Thanks for visiting! Come back any time. Have a great day! 👋"
    },
    {
      keys: ['thank','thanks','great','awesome','perfect','nice','cool','excellent'],
      reply: "You're very welcome! Anything else I can help with?"
    },
    {
      keys: ['who are you','what are you','your name','about dee','are you a bot','are you ai'],
      reply: "I'm Dee, an AI assistant built into this portfolio. I can answer questions about projects, skills, experience, and help you connect!"
    },
    {
      keys: ['project','work','built','created','made','portfolio','showcase'],
      reply: "Key projects here include an AI Chatbot Platform, n8n Workflow Automation, a LangChain Autonomous Agent, and a Google AI Studio integration. Head to the Projects page for full details — problem, solution, and outcomes!"
    },
    {
      keys: ['skill','technology','tech stack','language','framework','expertise','know how'],
      reply: "The skill set spans Python, Django, LangChain, OpenAI API, Google Gemini, n8n, JavaScript, Docker, and more. Visit the Skills page for the full breakdown with proficiency levels!"
    },
    {
      keys: ['contact','reach','email','hire','collaborate','get in touch','work together'],
      reply: "Head to the Contact page to send a message or book an appointment — both options are right there on the same page!"
    },
    {
      keys: ['appointment','book','schedule','meeting','call','chat'],
      reply: "Booking is easy — go to the Contact page and click the 'Book Appointment' tab. Fill in your preferred date and time and the request comes straight through!"
    },
    {
      keys: ['resume','cv','experience','education','qualification','background','career'],
      reply: "The Resume page has a full professional timeline — work experience, education, certifications, and achievements, all cleanly formatted!"
    },
    {
      keys: ['ai','machine learning','langchain','n8n','automation','chatbot','agent','llm','gpt'],
      reply: "AI and automation are a core focus here! Projects include a LangChain autonomous agent, n8n workflow automations, AI chatbots, and Google AI Studio integrations. Check the Projects page for the full story!"
    },
    {
      keys: ['about','who is','tell me','background','story'],
      reply: "Head to the About page for the full story — background, values, and what drives the work. Social links and contact info are there too!"
    },
    {
      keys: ['location','where','based','country','city','remote'],
      reply: "Location details are on the About page. Remote work and global collaborations are always welcome!"
    },
    {
      keys: ['github','linkedin','social','follow','twitter'],
      reply: "Social links are in the footer and on the About page. Check GitHub for code and LinkedIn for professional updates!"
    },
    {
      keys: ['help','what can you do','can you','options'],
      reply: "I can help with:\n📌 Project details & tech used\n💡 Skills & expertise\n📄 Resume & experience\n📅 Booking a meeting\n📬 Getting in touch\n\nWhat would you like to know?"
    },
  ];

  var FALLBACKS = [
    "That's a great question! Try asking me about projects, skills, experience, or how to book a meeting.",
    "I'm not 100% sure about that one. Feel free to use the Contact page to ask directly!",
    "Hmm, you could ask me about projects, skills, the resume, or how to get in touch. What would you like to know?",
  ];

  function localReply(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < KB.length; i++) {
      if (KB[i].keys.some(function (kw) { return lower.includes(kw); })) {
        return KB[i].reply;
      }
    }
    return FALLBACKS[Math.floor(Math.random() * FALLBACKS.length)];
  }

  /* ── Send message ─────────────────────────────────────────── */
  function sendMessage() {
    var text = input.value.trim();
    if (!text || isBusy) return;

    input.value = '';
    setLocked(true);
    addMsg(text, 'user');

    var thinkDelay = 300 + Math.random() * 200;
    var replyDelay = 600 + Math.random() * 600;

    setTimeout(function () {
      showTyping();
      body_.scrollTop = body_.scrollHeight;
    }, thinkDelay);

    var url  = (typeof CHATBOT_URL !== 'undefined') ? CHATBOT_URL : '/chatbot/';
    var csrf = (typeof CSRF_TOKEN  !== 'undefined') ? CSRF_TOKEN  : getCookie('csrftoken');
    var historySnapshot = conversationHistory.slice();

    fetch(url, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
      body:    JSON.stringify({ message: text, history: historySnapshot }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error('bad response');
        return res.json();
      })
      .then(function (data) {
        setTimeout(function () {
          removeTyping();
          var reply = data.reply || localReply(text);
          addMsg(reply, 'bot');
          conversationHistory.push({ role: 'user', text: text });
          conversationHistory.push({ role: 'bot',  text: reply });
          if (conversationHistory.length > 20) conversationHistory = conversationHistory.slice(-20);
          setLocked(false);
        }, replyDelay);
      })
      .catch(function () {
        setTimeout(function () {
          removeTyping();
          var reply = localReply(text);
          addMsg(reply, 'bot');
          conversationHistory.push({ role: 'user', text: text });
          conversationHistory.push({ role: 'bot',  text: reply });
          setLocked(false);
        }, replyDelay);
      });
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });

  /* ── Attention badge after 5 s if still closed ────────────── */
  setTimeout(function () {
    if (!isOpen && badge) badge.style.display = 'flex';
  }, 5000);

  function getCookie(name) {
    var m = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return m ? m[2] : '';
  }
})();

/* ---------- 6. STATS COUNTER ANIMATION ---------- */
(function () {
  var counters = document.querySelectorAll('.stat-number[data-target]');
  if (!counters.length) return;

  var observed = false;
  var observer = new IntersectionObserver(function (entries) {
    if (observed) return;
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        observed = true;
        counters.forEach(function (el) {
          var target = parseInt(el.getAttribute('data-target'), 10) || 0;
          var start = 0;
          var duration = 1400;
          var step = Math.ceil(duration / Math.max(target, 1));
          var timer = setInterval(function () {
            start += Math.ceil(target / (duration / 16));
            if (start >= target) { start = target; clearInterval(timer); }
            el.textContent = start;
          }, 16);
        });
        observer.disconnect();
      }
    });
  }, { threshold: 0.3 });

  observer.observe(counters[0].closest('.stats-grid') || counters[0]);
})();

/* ---------- 6b. TYPED TEXT EFFECT ---------- */
(function () {
  var el = document.querySelector('.typed-text');
  if (!el) return;
  var fullText = el.dataset.text || el.textContent;
  el.textContent = '';

  var i = 0;
  var cursor = document.createElement('span');
  cursor.textContent = '|';
  cursor.style.cssText = 'animation:blink 1s step-end infinite; color:var(--accent)';
  el.after(cursor);

  var style = document.createElement('style');
  style.textContent = '@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }';
  document.head.appendChild(style);

  function type() {
    if (i < fullText.length) {
      el.textContent += fullText[i++];
      setTimeout(type, 40 + Math.random() * 30);
    } else {
      setTimeout(function () {
        cursor.style.display = 'none';
      }, 1200);
    }
  }

  setTimeout(type, 600);
})();

/* ---------- 7. IMAGE LIGHTBOX ---------- */
(function () {
  var lb      = document.getElementById('lightbox');
  var lbImg   = document.getElementById('lightboxImg');
  var lbClose = document.getElementById('lightboxClose');
  if (!lb || !lbImg) return;

  function openLightbox(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt || '';
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lb.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(function () { lbImg.src = ''; }, 250);
  }

  // Wire up any element with data-lightbox attribute (img, div, etc.)
  document.querySelectorAll('[data-lightbox]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      openLightbox(el.dataset.lightbox, el.dataset.lightboxAlt || el.getAttribute('alt') || '');
    });
  });

  // Close on backdrop click
  lb.addEventListener('click', function (e) {
    if (e.target === lb) closeLightbox();
  });

  // Close button
  if (lbClose) lbClose.addEventListener('click', closeLightbox);

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lb.classList.contains('open')) closeLightbox();
  });
})();
