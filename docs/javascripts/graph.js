// Knowledge Space — 3D Neural Galaxy
// Pure Three.js with inline orbit controls

function _initGalaxy() {
  "use strict";
  var container = document.getElementById("knowledge-graph");
  if (!container || typeof THREE === "undefined") return;
  if (container.querySelector("canvas")) return; // already initialized

  // ── Data ──
  var FALLBACK = {
    "data-science":     { name: "Data Science",      articles: 50, color: "#a07ad0" },
    "python":           { name: "Python",             articles: 30, color: "#50b89a" },
    "web-frontend":     { name: "Web Frontend",       articles: 30, color: "#6090c8" },
    "devops":           { name: "DevOps",             articles: 35, color: "#c88060" },
    "architecture":     { name: "Architecture",       articles: 32, color: "#7088c8" },
    "data-engineering": { name: "Data Engineering",   articles: 33, color: "#8878b8" },
    "kafka":            { name: "Kafka",              articles: 38, color: "#d07870" },
    "sql-databases":    { name: "SQL & Databases",    articles: 32, color: "#9888c0" },
    "linux-cli":        { name: "Linux CLI",          articles: 27, color: "#a08878" },
    "llm-agents":       { name: "LLM & Agents",      articles: 32, color: "#c0b060" },
    "java-spring":      { name: "Java & Spring",      articles: 25, color: "#68b080" },
    "bi-analytics":     { name: "BI & Analytics",     articles: 23, color: "#70a0b0" },
    "algorithms":       { name: "Algorithms",         articles: 29, color: "#80a0d0" },
    "security":         { name: "Security",           articles: 29, color: "#b87080" },
    "seo-marketing":    { name: "SEO & Marketing",    articles: 20, color: "#80b868" },
    "testing-qa":       { name: "Testing & QA",       articles: 22, color: "#9090b8" },
    "rust":             { name: "Rust",               articles: 22, color: "#d89848" },
    "php":              { name: "PHP",                articles: 15, color: "#7090c0" },
    "nodejs":           { name: "Node.js",            articles: 16, color: "#58c098" },
    "ios-mobile":       { name: "iOS & Mobile",       articles: 21, color: "#b080b0" },
    "image-generation": { name: "Image Generation",   articles: 27, color: "#c8a058" },
    "misc":             { name: "Misc",               articles: 20, color: "#8898a8" },
    "cpp":              { name: "C++",                articles: 25, color: "#7090c0" },
    "natural-language-writing": { name: "Natural Language & Writing", articles: 8, color: "#90b8a0" },
    "llm-memory":       { name: "LLM Memory",         articles: 9, color: "#c8b070" },
    "audio-voice":      { name: "Voice & Audio",       articles: 6, color: "#a080c0" },
    "go":               { name: "Go",                  articles: 5, color: "#60b8c8" },
  };
  var stats = window.KS_STATS || {};
  var raw = (stats.domains && Object.keys(stats.domains).length > 0) ? stats.domains : FALLBACK;
  var domains = [];
  Object.keys(raw).forEach(function(slug) {
    var d = raw[slug];
    domains.push({ slug: slug, name: d.name, articles: d.articles, color: (FALLBACK[slug]||{}).color || "#8898a8" });
  });

  var linkDefs = [
    ["Kafka","Architecture"],["Kafka","Data Engineering"],["Kafka","Java & Spring"],
    ["Python","Data Science"],["Python","Data Engineering"],["Python","LLM & Agents"],
    ["SQL & Databases","Data Engineering"],["SQL & Databases","BI & Analytics"],
    ["DevOps","Linux CLI"],["DevOps","Architecture"],["DevOps","Security"],
    ["Architecture","Testing & QA"],["Architecture","Algorithms"],
    ["Data Science","LLM & Agents"],["Data Science","Data Engineering"],["Data Science","Algorithms"],
    ["LLM & Agents","Architecture"],
    ["Web Frontend","Node.js"],["Web Frontend","SEO & Marketing"],
    ["Java & Spring","Architecture"],
    ["Rust","Algorithms"],["Rust","Linux CLI"],
    ["PHP","SQL & Databases"],["PHP","Web Frontend"],
    ["Security","Linux CLI"],
    ["BI & Analytics","Data Engineering"],["Data Engineering","DevOps"],
    ["Image Generation","Data Science"],["Image Generation","LLM & Agents"],
    ["Misc","Python"],["Misc","Algorithms"],
    ["C++","Algorithms"],["C++","Architecture"],
    ["Natural Language & Writing","SEO & Marketing"],
    ["LLM Memory","LLM & Agents"],["LLM Memory","Architecture"],
    ["Voice & Audio","Data Science"],["Voice & Audio","Python"],
    ["Go","DevOps"],["Go","Architecture"],
  ];

  // ── Scene ──
  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060610, 0.0008);
  var camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 2000);
  camera.position.set(0, 10, 260);

  var renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x060610);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  container.appendChild(renderer.domElement);

  // ── Lighting — soft, no harsh specular ──
  scene.add(new THREE.AmbientLight(0x445566, 3.0));
  var dl = new THREE.DirectionalLight(0xccddee, 0.8);
  dl.position.set(60, 100, 80);
  scene.add(dl);
  var pl1 = new THREE.PointLight(0x6644aa, 0.8, 500);
  pl1.position.set(-100, 60, -80);
  scene.add(pl1);
  var pl2 = new THREE.PointLight(0x338888, 0.6, 500);
  pl2.position.set(60, -80, 120);
  scene.add(pl2);

  // ── Stars ──
  function addStars(n, spread, sz, col, op) {
    var g = new THREE.BufferGeometry(), p = new Float32Array(n * 3);
    for (var i = 0; i < n * 3; i++) p[i] = (Math.random() - 0.5) * spread;
    g.setAttribute("position", new THREE.BufferAttribute(p, 3));
    scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: col, size: sz, transparent: true, opacity: op, sizeAttenuation: true })));
  }
  addStars(3000, 1600, 0.8, 0x555588, 0.5);
  addStars(500, 900, 2.0, 0x7777aa, 0.4);
  addStars(100, 500, 3.5, 0x9999cc, 0.3);

  // ── Count connections per domain ──
  var connCount = {};
  domains.forEach(function(d) { connCount[d.name] = 0; });
  linkDefs.forEach(function(l) {
    if (connCount[l[0]] !== undefined) connCount[l[0]]++;
    if (connCount[l[1]] !== undefined) connCount[l[1]]++;
  });

  // ── Planets ──
  var SPREAD = 140;
  var planetNodes = [];
  var goldenAngle = Math.PI * (3 - Math.sqrt(5));

  domains.forEach(function (d, i) {
    var y = 1 - (i / (domains.length - 1)) * 2;
    var rAtY = Math.sqrt(1 - y * y);
    var theta = goldenAngle * i;
    var pos = new THREE.Vector3(
      Math.cos(theta) * rAtY * SPREAD + (Math.random() - 0.5) * 18,
      y * SPREAD * 0.5 + (Math.random() - 0.5) * 12,
      Math.sin(theta) * rAtY * SPREAD + (Math.random() - 0.5) * 18
    );

    var size = 3 + (d.articles / 50) * 14;
    var color = new THREE.Color(d.color);
    var group = new THREE.Group();
    group.position.copy(pos);
    // Slight overall tilt — each planet system in different plane
    group.rotation.x = (Math.random() - 0.5) * 0.15;
    group.rotation.z = (Math.random() - 0.5) * 0.12;

    // ── Planet with procedural texture ──
    var planetTex = generatePlanetTexture(d.color, i);
    var sphereGeo = new THREE.SphereGeometry(size, 48, 48);
    var sphereMat = new THREE.MeshStandardMaterial({
      map: planetTex,
      emissive: color.clone().multiplyScalar(0.05),
      roughness: 0.9,
      metalness: 0.02,
    });
    var sphere = new THREE.Mesh(sphereGeo, sphereMat);
    // Axial tilt — each planet tilted differently
    var tiltX = (Math.random() - 0.5) * 0.5; // up to ~15 degrees
    var tiltZ = (Math.random() - 0.5) * 0.4;
    sphere.rotation.x = tiltX;
    sphere.rotation.z = tiltZ;
    // Self-rotation — varied speeds AND directions
    sphere.userData.rotSpeed = (0.001 + Math.random() * 0.003) * (Math.random() > 0.3 ? 1 : -1);
    sphere.userData.tiltX = tiltX;
    sphere.userData.tiltZ = tiltZ;
    group.add(sphere);

    // ── Atmosphere shell — thin, bright edge ──
    var atmosGeo = new THREE.SphereGeometry(size * 1.04, 32, 32);
    var atmosMat = new THREE.MeshBasicMaterial({
      color: color.clone().offsetHSL(0, 0.15, 0.25),
      transparent: true, opacity: 0.08, side: THREE.BackSide, depthWrite: false,
    });
    group.add(new THREE.Mesh(atmosGeo, atmosMat));

    // ── Outer glow ──
    var glowGeo = new THREE.SphereGeometry(size * 2, 20, 20);
    var glowMat = new THREE.MeshBasicMaterial({
      color: color.clone().offsetHSL(0, 0.1, 0.15),
      transparent: true, opacity: 0.035, side: THREE.BackSide, depthWrite: false,
    });
    group.add(new THREE.Mesh(glowGeo, glowMat));

    // ── Saturn-style flat disc rings by CONNECTION count ──
    var nc = connCount[d.name] || 0;
    var ringCount = nc >= 5 ? 3 : nc >= 3 ? 2 : nc >= 1 ? 1 : 0;
    var ringTiltBase = Math.PI * (0.25 + Math.random() * 0.3);
    var ringTiltZ = (Math.random() - 0.5) * 0.4;

    for (var ri = 0; ri < ringCount; ri++) {
      // Each ring — unique texture
      var rtc = document.createElement("canvas");
      rtc.width = 512; rtc.height = 64;
      var rctx = rtc.getContext("2d");
      // Seeded random for this ring
      var rseed = i * 100 + ri * 17 + 1;
      var rrng = function() { rseed = (rseed * 16807) % 2147483647; return (rseed - 1) / 2147483646; };
      for (var rx = 0; rx < 512; rx++) {
        var t = rx / 512;
        var bandAlpha = 0;
        var numBands = 3 + Math.floor(rrng() * 4);
        for (var band = 0; band < numBands; band++) {
          var bc = 0.08 + band * (0.84 / numBands) + rrng() * 0.05;
          var bw = 0.03 + rrng() * 0.06;
          var dd = Math.abs(t - bc);
          if (dd < bw) bandAlpha = Math.max(bandAlpha, (1 - dd / bw) * (0.5 + rrng() * 0.3));
        }
        var rc = Math.floor(color.r * 255 + 20 + rrng() * 20);
        var gc = Math.floor(color.g * 255 + 15 + rrng() * 15);
        var bcc = Math.floor(color.b * 255 + 15 + rrng() * 15);
        rctx.fillStyle = "rgba("+Math.min(255,rc)+","+Math.min(255,gc)+","+Math.min(255,bcc)+","+bandAlpha+")";
        rctx.fillRect(rx, 0, 1, 64);
      }
      var ringTex = new THREE.CanvasTexture(rtc);

      var innerR = size * (1.15 + ri * 0.3);
      var outerR = size * (1.4 + ri * 0.35);
      var discGeo = new THREE.RingGeometry(innerR, outerR, 80, 1);
      var discMat = new THREE.MeshBasicMaterial({
        map: ringTex, side: THREE.DoubleSide,
        transparent: true, opacity: 0.55 - ri * 0.1, depthWrite: false,
      });
      var disc = new THREE.Mesh(discGeo, discMat);
      // Each ring slightly different tilt
      disc.rotation.x = ringTiltBase + ri * 0.08;
      disc.rotation.z = ringTiltZ + ri * 0.12;
      // Different rotation speeds AND directions
      disc.userData.speed = (0.0005 + ri * 0.0003 + Math.random() * 0.0004) * (ri % 2 === 0 ? 1 : -1);
      group.add(disc);
    }

    // ── Particle cloud ──
    var cloudN = 20 + Math.floor(d.articles * 0.4);
    var cGeo = new THREE.BufferGeometry(), cPos = new Float32Array(cloudN * 3);
    for (var j = 0; j < cloudN; j++) {
      var cr = size * (1.1 + Math.random() * 1.3);
      var ct = Math.random() * Math.PI * 2;
      var cp = Math.acos(2 * Math.random() - 1);
      cPos[j*3] = cr * Math.sin(cp) * Math.cos(ct);
      cPos[j*3+1] = cr * Math.sin(cp) * Math.sin(ct);
      cPos[j*3+2] = cr * Math.cos(cp);
    }
    cGeo.setAttribute("position", new THREE.BufferAttribute(cPos, 3));
    var cloud = new THREE.Points(cGeo, new THREE.PointsMaterial({
      color: color.clone().offsetHSL(0, 0, 0.2),
      size: 0.8, transparent: true, opacity: 0.4, sizeAttenuation: true, depthWrite: false,
    }));
    group.add(cloud);

    // ── Name ABOVE ──
    var nameS = makeText(d.name, 80, "800", "rgba(255,255,255,0.95)", 1024, 128);
    nameS.position.set(0, size + size * 0.5, 0);
    nameS.scale.set(Math.max(size * 4.5, 28), Math.max(size * 0.55, 3.5), 1);
    group.add(nameS);

    // ── Article count below name ──
    var countS = makeText(d.articles + " articles", 48, "500", "rgba(255,255,255,0.55)", 512, 80);
    countS.position.set(0, size + size * 0.05, 0);
    countS.scale.set(Math.max(size * 3, 18), Math.max(size * 0.35, 2.5), 1);
    group.add(countS);

    scene.add(group);
    planetNodes.push({
      group: group, sphere: sphere, cloud: cloud,
      pos: pos.clone(), size: size, color: color,
      name: d.name, slug: d.slug,
      driftPhase: Math.random() * Math.PI * 2,
      driftAmp: 1 + Math.random() * 2,
    });
  });

  // ── Procedural planet texture generator — 6 types ──
  function generatePlanetTexture(hexColor, seed) {
    var sz = 512;
    var c = document.createElement("canvas");
    c.width = sz; c.height = sz;
    var ctx = c.getContext("2d");

    var base = new THREE.Color(hexColor);
    var R = Math.floor(base.r * 255);
    var G = Math.floor(base.g * 255);
    var B = Math.floor(base.b * 255);

    ctx.fillStyle = hexColor;
    ctx.fillRect(0, 0, sz, sz);

    var rng = (function(s) {
      return function() { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
    })(seed * 7919 + 1);

    var type = seed % 6;

    // TYPE 0: Earth-like — oceans + continents + clouds
    if (type === 0) {
      // Ocean base (slightly darker)
      ctx.fillStyle = "rgba(" + Math.max(0,R-25) + "," + Math.max(0,G-15) + "," + Math.min(255,B+20) + ",0.5)";
      ctx.fillRect(0, 0, sz, sz);
      // Continents — irregular landmasses
      for (var pass = 0; pass < 4; pass++) {
        var lr = Math.max(0,R+20-pass*10), lg = Math.max(0,G+15-pass*8), lb = Math.max(0,B-20);
        for (var ci = 0; ci < 5 + Math.floor(rng() * 5); ci++) {
          var cx = rng() * sz, cy = rng() * sz, cr = 25 + rng() * 70;
          ctx.beginPath();
          ctx.ellipse(cx, cy, cr, cr * (0.4 + rng() * 0.6), rng() * Math.PI, 0, Math.PI * 2);
          ctx.fillStyle = "rgba("+lr+","+lg+","+lb+",0.35)";
          ctx.fill();
        }
      }
      // Clouds
      for (var cli = 0; cli < 10; cli++) {
        ctx.beginPath();
        ctx.ellipse(rng()*sz, rng()*sz, 30+rng()*100, 8+rng()*20, rng()*0.4, 0, Math.PI*2);
        ctx.fillStyle = "rgba(255,255,255,0.1)";
        ctx.fill();
      }
    }

    // TYPE 1: Gas giant — Jupiter-style banded
    if (type === 1) {
      for (var bi = 0; bi < 20; bi++) {
        var by = (bi / 20) * sz;
        var bh = sz / 20 + rng() * 8;
        var shift = Math.floor((rng() - 0.5) * 45);
        var wave = Math.sin(bi * 0.8) * 15;
        ctx.fillStyle = "rgba("+Math.max(0,Math.min(255,R+shift+wave))+","+Math.max(0,Math.min(255,G+shift*0.7))+","+Math.max(0,Math.min(255,B+shift*0.5))+",0.45)";
        ctx.fillRect(0, by, sz, bh);
      }
      // Great Red Spot style storms
      for (var si = 0; si < 1 + Math.floor(rng() * 2); si++) {
        var sx = rng()*sz, sy = rng()*sz, srx = 15+rng()*30, sry = 10+rng()*15;
        var grad = ctx.createRadialGradient(sx, sy, 0, sx, sy, srx);
        grad.addColorStop(0, "rgba("+Math.min(255,R+60)+","+Math.min(255,G+30)+","+Math.max(0,B-20)+",0.6)");
        grad.addColorStop(0.6, "rgba("+R+","+G+","+B+",0.2)");
        grad.addColorStop(1, "rgba("+R+","+G+","+B+",0)");
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.ellipse(sx, sy, srx, sry, rng()*0.3, 0, Math.PI*2); ctx.fill();
      }
    }

    // TYPE 2: Ice giant — Neptune/Uranus swirls
    if (type === 2) {
      // Subtle horizontal bands
      for (var ib = 0; ib < 8; ib++) {
        ctx.fillStyle = "rgba("+Math.min(255,R+Math.floor(rng()*30))+","+Math.min(255,G+Math.floor(rng()*30))+","+Math.min(255,B+Math.floor(rng()*40))+",0.2)";
        ctx.fillRect(0, ib*(sz/8), sz, sz/8);
      }
      // Swirl patterns
      for (var sw = 0; sw < 6; sw++) {
        ctx.strokeStyle = "rgba("+Math.min(255,R+40)+","+Math.min(255,G+50)+","+Math.min(255,B+60)+",0.12)";
        ctx.lineWidth = 3 + rng() * 5;
        ctx.beginPath();
        var swx = rng()*sz, swy = rng()*sz;
        for (var sp = 0; sp < 20; sp++) {
          var angle = sp * 0.3 + rng() * 0.2;
          var radius = 5 + sp * 3;
          ctx.lineTo(swx + Math.cos(angle) * radius, swy + Math.sin(angle) * radius);
        }
        ctx.stroke();
      }
    }

    // TYPE 3: Desert/Mars — red/brown with craters
    if (type === 3) {
      // Sandy/dusty patches
      for (var dp = 0; dp < 12; dp++) {
        var dx = rng()*sz, dy = rng()*sz, dr = 30+rng()*60;
        ctx.beginPath(); ctx.arc(dx, dy, dr, 0, Math.PI*2);
        ctx.fillStyle = "rgba("+Math.min(255,R+20)+","+Math.max(0,G-10)+","+Math.max(0,B-15)+",0.25)";
        ctx.fill();
      }
      // Craters
      for (var cri = 0; cri < 8 + Math.floor(rng()*6); cri++) {
        var crx = rng()*sz, cry = rng()*sz, crr = 5+rng()*20;
        // Crater shadow
        ctx.beginPath(); ctx.arc(crx, cry, crr, 0, Math.PI*2);
        ctx.fillStyle = "rgba(0,0,0,0.15)"; ctx.fill();
        // Crater rim (lighter)
        ctx.beginPath(); ctx.arc(crx-1, cry-1, crr*0.85, 0, Math.PI*2);
        ctx.fillStyle = "rgba("+Math.min(255,R+30)+","+Math.min(255,G+20)+","+Math.min(255,B+10)+",0.2)"; ctx.fill();
      }
      // Polar ice cap
      var capGrad = ctx.createRadialGradient(sz/2, 0, 0, sz/2, 0, sz*0.35);
      capGrad.addColorStop(0, "rgba(220,230,240,0.3)");
      capGrad.addColorStop(1, "rgba(220,230,240,0)");
      ctx.fillStyle = capGrad;
      ctx.fillRect(0, 0, sz, sz/3);
    }

    // TYPE 4: Volcanic — dark with glowing lava cracks
    if (type === 4) {
      // Darken base
      ctx.fillStyle = "rgba(0,0,0,0.35)";
      ctx.fillRect(0, 0, sz, sz);
      // Lava cracks — bright lines
      for (var lci = 0; lci < 12 + Math.floor(rng()*8); lci++) {
        ctx.strokeStyle = "rgba("+Math.min(255,R+80)+","+Math.min(255,G+40)+","+Math.max(0,B-30)+",0.4)";
        ctx.lineWidth = 1 + rng() * 2.5;
        ctx.shadowColor = "rgba("+Math.min(255,R+100)+","+Math.min(255,G+50)+",0,0.6)";
        ctx.shadowBlur = 4;
        ctx.beginPath();
        var lx = rng()*sz, ly = rng()*sz;
        ctx.moveTo(lx, ly);
        for (var ls = 0; ls < 4 + rng()*6; ls++) {
          lx += (rng()-0.5)*50; ly += (rng()-0.5)*35;
          ctx.lineTo(lx, ly);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;
      }
      // Volcanic hotspots
      for (var hi = 0; hi < 3; hi++) {
        var hx = rng()*sz, hy = rng()*sz, hr = 8+rng()*15;
        var hGrad = ctx.createRadialGradient(hx, hy, 0, hx, hy, hr);
        hGrad.addColorStop(0, "rgba("+Math.min(255,R+100)+","+Math.min(255,G+60)+",20,0.7)");
        hGrad.addColorStop(1, "rgba("+R+","+G+","+B+",0)");
        ctx.fillStyle = hGrad; ctx.fillRect(hx-hr, hy-hr, hr*2, hr*2);
      }
    }

    // TYPE 5: Frozen/crystalline — white-blue with geometric patches
    if (type === 5) {
      // Bright icy overlay
      ctx.fillStyle = "rgba(200,210,230,0.2)";
      ctx.fillRect(0, 0, sz, sz);
      // Crystal formations — angular shapes
      for (var fi = 0; fi < 10; fi++) {
        ctx.beginPath();
        var fx = rng()*sz, fy = rng()*sz;
        ctx.moveTo(fx, fy);
        for (var fv = 0; fv < 4 + Math.floor(rng()*3); fv++) {
          ctx.lineTo(fx + (rng()-0.5)*60, fy + (rng()-0.5)*50);
        }
        ctx.closePath();
        ctx.fillStyle = "rgba("+Math.min(255,R+40)+","+Math.min(255,G+50)+","+Math.min(255,B+60)+",0.18)";
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.08)";
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
      // Frost highlights
      for (var fri = 0; fri < 15; fri++) {
        ctx.beginPath();
        ctx.arc(rng()*sz, rng()*sz, 2+rng()*6, 0, Math.PI*2);
        ctx.fillStyle = "rgba(240,245,255,0.15)";
        ctx.fill();
      }
    }

    // Noise grain for all types
    var imgData = ctx.getImageData(0, 0, sz, sz);
    var data = imgData.data;
    for (var pi = 0; pi < data.length; pi += 4) {
      var noise = (rng() - 0.5) * 12;
      data[pi] = Math.max(0, Math.min(255, data[pi] + noise));
      data[pi+1] = Math.max(0, Math.min(255, data[pi+1] + noise));
      data[pi+2] = Math.max(0, Math.min(255, data[pi+2] + noise));
    }
    ctx.putImageData(imgData, 0, 0);

    var tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.ClampToEdgeWrapping;
    return tex;
  }

  function makeText(text, fontSize, fontWeight, fillStyle, cw, ch) {
    var c = document.createElement("canvas"); c.width = cw; c.height = ch;
    var ctx = c.getContext("2d");
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.font = fontWeight + " " + fontSize + "px Inter, system-ui, sans-serif";
    ctx.shadowColor = "rgba(0,0,0,0.9)"; ctx.shadowBlur = 10;
    ctx.fillStyle = fillStyle;
    ctx.fillText(text, cw / 2, ch / 2);
    var tex = new THREE.CanvasTexture(c);
    var s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: true, depthWrite: false }));
    return s;
  }

  // ── Neural connections near mouse ──
  var mouse = new THREE.Vector2(9999, 9999);
  var raycaster = new THREE.Raycaster();
  var connLines = linkDefs.map(function () {
    var geo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    var mat = new THREE.LineBasicMaterial({ color: 0x8888cc, transparent: true, opacity: 0, depthWrite: false });
    var line = new THREE.Line(geo, mat); line.renderOrder = -1;
    scene.add(line); return line;
  });

  container.addEventListener("mousemove", function (e) {
    var r = container.getBoundingClientRect();
    mouse.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    mouse.y = -((e.clientY - r.top) / r.height) * 2 + 1;
  });
  container.addEventListener("mouseleave", function () { mouse.set(9999, 9999); });

  // ── Click → navigate ──
  var clickStart = { x: 0, y: 0 };
  container.addEventListener("mousedown", function (e) { clickStart = { x: e.clientX, y: e.clientY }; });
  container.addEventListener("mouseup", function (e) {
    if (Math.abs(e.clientX - clickStart.x) + Math.abs(e.clientY - clickStart.y) > 5) return;
    var r = container.getBoundingClientRect();
    var cm = new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    raycaster.setFromCamera(cm, camera);
    var hits = raycaster.intersectObjects(planetNodes.map(function(p){return p.sphere}));
    if (hits.length > 0) {
      var node = planetNodes.find(function(p){return p.sphere === hits[0].object});
      if (node) window.location.href = "/" + node.slug + "/";
    }
  });

  // ── Intro animation: particles → planets ──
  var introPhase = 0;
  var introDuration = 5.0; // slower, more cinematic
  var introStartTime = performance.now();

  // Scatter particles — each planet starts as a cloud of points
  var introParticles = [];
  planetNodes.forEach(function(p) {
    var count = 60 + Math.floor(p.size * 3);
    var positions = [];
    for (var ip = 0; ip < count; ip++) {
      // Start positions — scattered far from planet
      positions.push({
        sx: (Math.random() - 0.5) * 600,
        sy: (Math.random() - 0.5) * 400,
        sz: (Math.random() - 0.5) * 600,
      });
    }
    var geo = new THREE.BufferGeometry();
    var posArr = new Float32Array(count * 3);
    geo.setAttribute("position", new THREE.BufferAttribute(posArr, 3));
    var pts = new THREE.Points(geo, new THREE.PointsMaterial({
      color: p.color, size: 0.3, transparent: true, opacity: 0.5,
      sizeAttenuation: true, depthWrite: false, blending: THREE.AdditiveBlending,
    }));
    scene.add(pts);
    introParticles.push({ pts: pts, positions: positions, target: p, posArr: posArr });

    // Hide planet initially
    p.group.visible = false;
  });

  // ── Inline Orbit Controls (drag rotate, scroll zoom) ──
  var spherical = { theta: 0, phi: Math.PI / 2.2, radius: 260 };
  var isDragging = false, lastMouse = { x: 0, y: 0 };
  var targetTheta = spherical.theta, targetPhi = spherical.phi, targetRadius = spherical.radius;

  container.addEventListener("mousedown", function (e) {
    if (e.button === 0 || e.button === 2) { isDragging = e.button; lastMouse = { x: e.clientX, y: e.clientY }; }
  });
  window.addEventListener("mouseup", function () { isDragging = false; });
  window.addEventListener("mousemove", function (e) {
    if (isDragging === false) return;
    var dx = e.clientX - lastMouse.x, dy = e.clientY - lastMouse.y;
    lastMouse = { x: e.clientX, y: e.clientY };
    userDragOffset.theta -= dx * 0.008;
    userDragOffset.phi = Math.max(-1.2, Math.min(1.2, userDragOffset.phi - dy * 0.005));
  });
  container.addEventListener("wheel", function (e) {
    e.preventDefault();
    targetRadius = Math.max(80, Math.min(600, targetRadius + e.deltaY * 0.5));
  }, { passive: false });
  container.addEventListener("contextmenu", function (e) { e.preventDefault(); });

  // Touch support
  var lastTouch = null;
  container.addEventListener("touchstart", function (e) {
    if (e.touches.length === 1) {
      isDragging = 0;
      lastMouse = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      clickStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
  }, { passive: true });
  container.addEventListener("touchmove", function (e) {
    if (e.touches.length === 1 && isDragging !== false) {
      var dx = e.touches[0].clientX - lastMouse.x;
      var dy = e.touches[0].clientY - lastMouse.y;
      lastMouse = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      userDragOffset.theta -= dx * 0.008;
      userDragOffset.phi = Math.max(-1.2, Math.min(1.2, userDragOffset.phi - dy * 0.005));
    }
  }, { passive: true });
  container.addEventListener("touchend", function () { isDragging = false; }, { passive: true });

  // ══════════════════════════════════════════
  // WOW EFFECTS SETUP
  // ══════════════════════════════════════════

  // ── 1. Nebula fog clouds ──
  var nebulae = [];
  var nebulaColors = [0x442266, 0x224466, 0x443322, 0x225544, 0x553344];
  for (var ni = 0; ni < 5; ni++) {
    var nebGeo = new THREE.PlaneGeometry(200 + Math.random() * 200, 200 + Math.random() * 200);
    var nebCanvas = document.createElement("canvas");
    nebCanvas.width = 256; nebCanvas.height = 256;
    var nctx = nebCanvas.getContext("2d");
    var grad = nctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    var nc = new THREE.Color(nebulaColors[ni]);
    grad.addColorStop(0, "rgba("+Math.floor(nc.r*255)+","+Math.floor(nc.g*255)+","+Math.floor(nc.b*255)+",0.15)");
    grad.addColorStop(0.5, "rgba("+Math.floor(nc.r*255)+","+Math.floor(nc.g*255)+","+Math.floor(nc.b*255)+",0.05)");
    grad.addColorStop(1, "rgba(0,0,0,0)");
    nctx.fillStyle = grad;
    nctx.fillRect(0, 0, 256, 256);
    var nebTex = new THREE.CanvasTexture(nebCanvas);
    var nebMat = new THREE.MeshBasicMaterial({
      map: nebTex, transparent: true, opacity: 0.6,
      side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending,
    });
    var nebMesh = new THREE.Mesh(nebGeo, nebMat);
    nebMesh.position.set((Math.random()-0.5)*500, (Math.random()-0.5)*300, (Math.random()-0.5)*500);
    nebMesh.rotation.set(Math.random()*Math.PI, Math.random()*Math.PI, Math.random()*Math.PI);
    nebMesh.renderOrder = -5;
    scene.add(nebMesh);
    nebulae.push(nebMesh);
  }

  // ── 2. Comets ──
  var comets = [];
  function spawnComet() {
    var dir = new THREE.Vector3((Math.random()-0.5)*2, (Math.random()-0.5)*0.5, (Math.random()-0.5)*2).normalize();
    var startPos = dir.clone().multiplyScalar(-400);
    var speed = 1.5 + Math.random() * 2;
    var tailLen = 15;
    var cometColor = new THREE.Color().setHSL(Math.random()*0.2 + 0.55, 0.6, 0.7);

    // Head
    var headGeo = new THREE.SphereGeometry(0.8, 8, 8);
    var headMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 });
    var head = new THREE.Mesh(headGeo, headMat);
    head.position.copy(startPos);
    scene.add(head);

    // Trail particles
    var trailGeo = new THREE.BufferGeometry();
    var trailPos = new Float32Array(tailLen * 3);
    for (var ti = 0; ti < tailLen; ti++) {
      trailPos[ti*3] = startPos.x; trailPos[ti*3+1] = startPos.y; trailPos[ti*3+2] = startPos.z;
    }
    trailGeo.setAttribute("position", new THREE.BufferAttribute(trailPos, 3));
    var trailMat = new THREE.PointsMaterial({
      color: cometColor, size: 1.5, transparent: true, opacity: 0.5,
      sizeAttenuation: true, depthWrite: false, blending: THREE.AdditiveBlending,
    });
    var trail = new THREE.Points(trailGeo, trailMat);
    scene.add(trail);

    comets.push({ head: head, trail: trail, trailPos: trailPos, dir: dir, speed: speed, life: 0, maxLife: 300 });
  }
  // Spawn first comet after intro
  setTimeout(function() { spawnComet(); }, 6000);

  // ── 3. Hover explosion particles ──
  var hoverTarget = null;
  var hoverParticles = null;
  var hoverExplosionPhase = 0;

  function createHoverExplosion(node) {
    if (hoverParticles) { scene.remove(hoverParticles); }
    var count = 50;
    var geo = new THREE.BufferGeometry();
    var pos = new Float32Array(count * 3);
    var velocities = [];
    for (var hi = 0; hi < count; hi++) {
      pos[hi*3] = 0; pos[hi*3+1] = 0; pos[hi*3+2] = 0;
      velocities.push(new THREE.Vector3(
        (Math.random()-0.5)*2, (Math.random()-0.5)*2, (Math.random()-0.5)*2
      ));
    }
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    var mat = new THREE.PointsMaterial({
      color: node.color, size: 1.5, transparent: true, opacity: 0.8,
      sizeAttenuation: true, depthWrite: false, blending: THREE.AdditiveBlending,
    });
    hoverParticles = new THREE.Points(geo, mat);
    hoverParticles.position.copy(node.group.position);
    hoverParticles.userData.velocities = velocities;
    scene.add(hoverParticles);
    hoverExplosionPhase = 0;
  }

  // ── 4. Neural pulse system ──
  var pulses = [];
  function firePulse(srcNode) {
    linkDefs.forEach(function(link) {
      var otherName = null;
      if (link[0] === srcNode.name) otherName = link[1];
      if (link[1] === srcNode.name) otherName = link[0];
      if (!otherName) return;
      var tgtNode = planetNodes.find(function(p){return p.name === otherName});
      if (!tgtNode) return;

      var pulseGeo = new THREE.SphereGeometry(0.6, 8, 8);
      var pulseMat = new THREE.MeshBasicMaterial({
        color: srcNode.color, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending,
      });
      var pulseMesh = new THREE.Mesh(pulseGeo, pulseMat);
      pulseMesh.position.copy(srcNode.group.position);
      scene.add(pulseMesh);
      pulses.push({
        mesh: pulseMesh, src: srcNode, tgt: tgtNode, t: 0, speed: 0.015 + Math.random() * 0.01,
      });
    });
  }

  // ── 5. Parallax star layers (store refs) ──
  // Stars already created above — we'll move them based on mouse
  // Re-reference the star layers by wrapping them in groups
  // (stars are the first 3 Points objects added to scene)
  var starLayers = [];
  scene.children.forEach(function(c) {
    if (c instanceof THREE.Points && !c.userData.isPlanetCloud) {
      starLayers.push(c);
    }
  });
  // Tag planet clouds so they don't get moved
  planetNodes.forEach(function(p) { p.cloud.userData.isPlanetCloud = true; });

  // ══════════════════════════════════════════

  // ── Tilted elliptical orbit — start farther away ──
  var orbitT = 0;
  var orbitSpeed = 0.0002;
  var ellipseA = 380;   // semi-major axis (wider)
  var ellipseB = 230;   // semi-minor axis
  var orbitTilt = 0.3;
  var orbitYBase = 30;
  var orbitYAmp = 45;
  var userDragOffset = { theta: 0, phi: 0 };
  var zoomFactor = 1.0;

  // ── Animate ──
  function animate() {
    requestAnimationFrame(animate);

    // ── Intro: particles converge into planets ──
    var now = performance.now();
    var elapsed = (now - introStartTime) / 1000;
    introPhase = Math.min(1, elapsed / introDuration);

    if (introPhase < 1) {
      // Smooth easing — slow start, fast middle, slow end
      var ease = introPhase < 0.5
        ? 4 * introPhase * introPhase * introPhase
        : 1 - Math.pow(-2 * introPhase + 2, 3) / 2;

      // Particles converge toward planet positions
      // Size: small dust → grow bright → shrink as absorbed into planet
      var sizeCurve;
      if (introPhase < 0.3) {
        sizeCurve = 0.3 + (introPhase / 0.3) * 2.0;
      } else if (introPhase < 0.65) {
        sizeCurve = 2.3 + ((introPhase - 0.3) / 0.35) * 1.2; // peak 3.5
      } else {
        // Shrink — particles get smaller as they merge into planet surface
        sizeCurve = 3.5 * Math.pow(1 - (introPhase - 0.65) / 0.35, 2);
      }

      // Opacity: fade in → bright → fade as absorbed
      var opacityCurve;
      if (introPhase < 0.2) {
        opacityCurve = introPhase / 0.2 * 0.5;
      } else if (introPhase < 0.65) {
        opacityCurve = 0.5 + ((introPhase - 0.2) / 0.45) * 0.4;
      } else {
        // Fade out gently — absorbed into solid planet
        opacityCurve = 0.9 * Math.pow(1 - (introPhase - 0.65) / 0.35, 1.5);
      }

      // Visible count: few → all (particles only appear, never disappear — they absorb into planet)
      var visibleRatio;
      if (introPhase < 0.2) {
        visibleRatio = 0.1 + (introPhase / 0.2) * 0.3;
      } else {
        visibleRatio = Math.min(1, 0.4 + ((introPhase - 0.2) / 0.5) * 0.6);
      }

      introParticles.forEach(function(ip) {
        var tx = ip.target.pos.x;
        var ty = ip.target.pos.y;
        var tz = ip.target.pos.z;
        var arr = ip.posArr;
        var totalCount = ip.positions.length;
        var visCount = Math.floor(totalCount * visibleRatio);

        for (var j = 0; j < totalCount; j++) {
          var sp = ip.positions[j];

          if (j < visCount) {
            // All particles converge TO the planet center — always moving inward
            var delay = (j / totalCount) * 0.35;
            var localEase = Math.max(0, Math.min(1, (introPhase - delay) / (1 - delay)));
            localEase = localEase * localEase * (3 - 2 * localEase);

            arr[j*3]   = sp.sx + (tx - sp.sx) * localEase;
            arr[j*3+1] = sp.sy + (ty - sp.sy) * localEase;
            arr[j*3+2] = sp.sz + (tz - sp.sz) * localEase;
          } else {
            arr[j*3] = 9999; arr[j*3+1] = 9999; arr[j*3+2] = 9999;
          }
        }
        ip.pts.geometry.attributes.position.needsUpdate = true;
        ip.pts.material.size = sizeCurve;
        ip.pts.material.opacity = opacityCurve;
      });

      // Planets grow from scale 0 → 1 during last 40% of intro
      if (introPhase > 0.6) {
        var scaleProgress = (introPhase - 0.6) / 0.4;
        scaleProgress = scaleProgress * scaleProgress * (3 - 2 * scaleProgress);
        planetNodes.forEach(function(p) {
          p.group.visible = true;
          p.group.scale.setScalar(scaleProgress);
        });
      }
    } else {
      // Intro done — cleanup particles, ensure planets at full scale
      if (introParticles.length > 0) {
        introParticles.forEach(function(ip) {
          scene.remove(ip.pts);
          ip.pts.geometry.dispose();
          ip.pts.material.dispose();
          ip.target.group.visible = true;
          ip.target.group.scale.setScalar(1);
        });
        introParticles = [];
        planetNodes.forEach(function(p) {
          p.group.visible = true;
          p.group.scale.setScalar(1);
        });
      }
    }

    // Auto-orbit along tilted ellipse when not dragging
    if (isDragging === false) {
      orbitT += orbitSpeed;
    }

    // Smooth drag offset decay — slow enough to feel controllable
    userDragOffset.theta *= 0.999;
    userDragOffset.phi *= 0.999;

    // Smooth zoom
    spherical.radius += (targetRadius - spherical.radius) * 0.05;
    zoomFactor = spherical.radius / 260;

    // Elliptical orbit position
    var t = orbitT + userDragOffset.theta;
    var cosOT = Math.cos(orbitTilt);
    var sinOT = Math.sin(orbitTilt);

    var ex = ellipseA * Math.sin(t) * zoomFactor;
    var ez = (ellipseB * Math.cos(t) * cosOT) * zoomFactor;
    var ey = orbitYBase + orbitYAmp * Math.sin(t * 0.7) + ellipseB * Math.cos(t) * sinOT * 0.5;
    ey += userDragOffset.phi * 80;
    ey *= zoomFactor;

    camera.position.set(ex, ey, ez);
    camera.lookAt(0, 0, 0);

    // Drift + ring rotation
    planetNodes.forEach(function (p) {
      p.driftPhase += 0.0006;
      p.group.position.x = p.pos.x + Math.sin(p.driftPhase) * p.driftAmp;
      p.group.position.y = p.pos.y + Math.cos(p.driftPhase * 0.7) * p.driftAmp * 0.3;
      p.group.position.z = p.pos.z + Math.sin(p.driftPhase * 0.4 + 1) * p.driftAmp * 0.5;
      p.group.children.forEach(function (c) {
        // Ring disc rotation — each at own speed/direction
        if (c.userData && c.userData.speed && !c.userData.rotSpeed) c.rotation.z += c.userData.speed;
        // Planet self-rotation around its tilted axis
        if (c.userData && c.userData.rotSpeed) c.rotation.y += c.userData.rotSpeed;
      });
      p.cloud.rotation.y += 0.0004;
      p.cloud.rotation.x += 0.00015;
    });

    // Neural connections
    linkDefs.forEach(function (link, idx) {
      var line = connLines[idx];
      var srcN = planetNodes.find(function(p){return p.name === link[0]});
      var tgtN = planetNodes.find(function(p){return p.name === link[1]});
      if (!srcN || !tgtN) { line.material.opacity = 0; return; }
      var sp = srcN.group.position, tp = tgtN.group.position;
      var mid = new THREE.Vector3((sp.x+tp.x)/2,(sp.y+tp.y)/2,(sp.z+tp.z)/2).project(camera);
      var dist = Math.sqrt(Math.pow(mid.x-mouse.x,2)+Math.pow(mid.y-mouse.y,2));
      var tgt = (dist < 0.7 && mouse.x < 5) ? (1-dist/0.7)*0.35 : 0;
      line.material.opacity += (tgt - line.material.opacity) * 0.08;
      if (line.material.opacity > 0.005) {
        var a = line.geometry.attributes.position.array;
        a[0]=sp.x;a[1]=sp.y;a[2]=sp.z;a[3]=tp.x;a[4]=tp.y;a[5]=tp.z;
        line.geometry.attributes.position.needsUpdate = true;
        line.material.color.copy(srcN.color).offsetHSL(0,-0.2,0.2);
      }
    });

    // ══ WOW EFFECTS ANIMATE ══

    // 1. Nebula slow drift
    nebulae.forEach(function(n, i) {
      n.rotation.z += 0.00005 * (i % 2 === 0 ? 1 : -1);
      n.position.y += Math.sin(orbitT * 0.5 + i) * 0.02;
    });

    // 2. Comets
    comets.forEach(function(c, ci) {
      c.life++;
      c.head.position.addScaledVector(c.dir, c.speed);
      // Update trail — shift positions
      for (var ti = c.trailPos.length/3 - 1; ti > 0; ti--) {
        c.trailPos[ti*3] = c.trailPos[(ti-1)*3];
        c.trailPos[ti*3+1] = c.trailPos[(ti-1)*3+1];
        c.trailPos[ti*3+2] = c.trailPos[(ti-1)*3+2];
      }
      c.trailPos[0] = c.head.position.x;
      c.trailPos[1] = c.head.position.y;
      c.trailPos[2] = c.head.position.z;
      c.trail.geometry.attributes.position.needsUpdate = true;
      // Fade out near end
      if (c.life > c.maxLife * 0.8) {
        var fade = 1 - (c.life - c.maxLife * 0.8) / (c.maxLife * 0.2);
        c.head.material.opacity = fade;
        c.trail.material.opacity = fade * 0.5;
      }
      if (c.life >= c.maxLife) {
        scene.remove(c.head); scene.remove(c.trail);
        comets.splice(ci, 1);
        // Respawn after random delay
        setTimeout(spawnComet, 5000 + Math.random() * 15000);
      }
    });

    // 3. Hover explosion
    raycaster.setFromCamera(mouse, camera);
    var hovers = raycaster.intersectObjects(planetNodes.map(function(p){return p.sphere}));
    var hoveredNode = hovers.length > 0 ? planetNodes.find(function(p){return p.sphere === hovers[0].object}) : null;
    container.style.cursor = hoveredNode ? "pointer" : "grab";

    if (hoveredNode && hoveredNode !== hoverTarget) {
      hoverTarget = hoveredNode;
      createHoverExplosion(hoveredNode);
      // Fire neural pulse on hover
      firePulse(hoveredNode);
    }
    if (!hoveredNode && hoverTarget) {
      hoverTarget = null;
    }

    // Animate hover explosion particles
    if (hoverParticles && hoverTarget) {
      hoverExplosionPhase += 0.02;
      var hpArr = hoverParticles.geometry.attributes.position.array;
      var vels = hoverParticles.userData.velocities;
      for (var hi = 0; hi < vels.length; hi++) {
        hpArr[hi*3] += vels[hi].x * 0.3;
        hpArr[hi*3+1] += vels[hi].y * 0.3;
        hpArr[hi*3+2] += vels[hi].z * 0.3;
        // Slow down
        vels[hi].multiplyScalar(0.98);
      }
      hoverParticles.geometry.attributes.position.needsUpdate = true;
      hoverParticles.material.opacity = Math.max(0, 0.8 - hoverExplosionPhase * 0.4);
      hoverParticles.position.copy(hoverTarget.group.position);

      // Scale up hovered planet slightly
      if (hoverTarget.group.scale.x < 1.15) {
        hoverTarget.group.scale.multiplyScalar(1.005);
      }
    }
    // Scale down non-hovered planets
    planetNodes.forEach(function(p) {
      if (p !== hoverTarget && p.group.scale.x > 1.001) {
        p.group.scale.multiplyScalar(0.995);
      }
    });

    // 4. Neural pulses traveling along connections
    for (var pi = pulses.length - 1; pi >= 0; pi--) {
      var pulse = pulses[pi];
      pulse.t += pulse.speed;
      if (pulse.t >= 1) {
        // Flash target planet briefly
        if (pulse.tgt.sphere.material.emissive) {
          pulse.tgt.sphere.material.emissive.copy(pulse.src.color).multiplyScalar(0.5);
          setTimeout((function(tgt) { return function() {
            tgt.sphere.material.emissive.copy(tgt.color).multiplyScalar(0.12);
          }; })(pulse.tgt), 300);
        }
        scene.remove(pulse.mesh);
        pulses.splice(pi, 1);
      } else {
        var sp = pulse.src.group.position;
        var tp = pulse.tgt.group.position;
        pulse.mesh.position.lerpVectors(sp, tp, pulse.t);
        pulse.mesh.material.opacity = pulse.t < 0.1 ? pulse.t * 9 : pulse.t > 0.8 ? (1 - pulse.t) * 5 : 0.9;
        // Grow slightly in middle
        var pScale = 1 + Math.sin(pulse.t * Math.PI) * 0.8;
        pulse.mesh.scale.setScalar(pScale);
      }
    }

    // 5. Parallax stars — subtle shift with mouse
    if (mouse.x < 5) {
      starLayers.forEach(function(layer, li) {
        var parallaxStrength = (li + 1) * 0.3;
        layer.position.x += (mouse.x * parallaxStrength * 5 - layer.position.x) * 0.02;
        layer.position.y += (mouse.y * parallaxStrength * 3 - layer.position.y) * 0.02;
      });
    }

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener("resize", function () {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}

// Run on initial load + re-run on MkDocs Material instant navigation
_initGalaxy();
if (typeof document$ !== "undefined") {
  document$.subscribe(function() { _initGalaxy(); });
} else {
  // Fallback: observe DOM for container re-insertion (instant navigation)
  var _galaxyObs = new MutationObserver(function() {
    var c = document.getElementById("knowledge-graph");
    if (c && !c.querySelector("canvas") && typeof THREE !== "undefined") _initGalaxy();
  });
  _galaxyObs.observe(document.body, { childList: true, subtree: true });
}

// ── Stats ──
function _initStats(){var s=window.KS_STATS;if(!s)return;var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v};el("ks-total-articles",s.total_articles);el("ks-total-domains",s.total_domains);el("ks-graph-nodes",s.total_articles)}
_initStats();
// ── Copy ──
function _initCopy(){var b=document.getElementById("snippet-copy-btn"),t=document.getElementById("claude-prompt-text");if(!b||!t||b._ksInit)return;b._ksInit=true;b.addEventListener("click",function(){navigator.clipboard.writeText(t.textContent.trim()).then(function(){b.classList.add("copied");b.querySelector("span").textContent="Copied!";setTimeout(function(){b.classList.remove("copied");b.querySelector("span").textContent="Copy Claude Prompt"},2000)})})}
_initCopy();
// ── Subscribe ──
function _initSubscribe(){var f=document.getElementById("subscribe-form"),w=document.getElementById("subscribe-form-wrap");if(!f||!w||f._ksInit)return;f._ksInit=true;f.addEventListener("submit",function(e){e.preventDefault();var m=document.getElementById("sub-msg"),b=document.getElementById("sub-btn"),email=document.getElementById("sub-email").value.trim();b.disabled=true;b.textContent="...";fetch("/api/subscribe",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:email})}).then(function(r){return r.json()}).then(function(d){if(d.ok){w.textContent="";var sp=document.createElement("span");sp.style.cssText="color:#03dac6;font-size:0.78rem;font-weight:600;";sp.textContent="Subscribed!";w.appendChild(sp)}else{if(m){m.textContent=d.error||"Error";m.className="ks-subscribe__msg error"}b.disabled=false;b.textContent="Subscribe"}}).catch(function(){if(m){m.textContent="Network error";m.className="ks-subscribe__msg error"}b.disabled=false;b.textContent="Subscribe"})})}
_initSubscribe();
// ── Re-init on instant navigation ──
if (typeof document$ !== "undefined") {
  document$.subscribe(function() { _initGalaxy(); _initStats(); _initCopy(); _initSubscribe(); });
}
