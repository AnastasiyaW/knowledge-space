// Knowledge Vault - Interactive Domain Graph
// Force-directed graph with signal particles on edges

(function () {
  const container = document.getElementById("knowledge-graph");
  if (!container) return;

  const domains = [
    { id: "Data Science", articles: 85, group: "data" },
    { id: "Python", articles: 43, group: "code" },
    { id: "Web Frontend", articles: 40, group: "code" },
    { id: "DevOps", articles: 39, group: "infra" },
    { id: "Architecture", articles: 39, group: "design" },
    { id: "Data Engineering", articles: 38, group: "data" },
    { id: "Kafka", articles: 33, group: "infra" },
    { id: "SQL & Databases", articles: 27, group: "data" },
    { id: "Linux CLI", articles: 25, group: "infra" },
    { id: "LLM & Agents", articles: 24, group: "ai" },
    { id: "Java & Spring", articles: 21, group: "code" },
    { id: "BI & Analytics", articles: 21, group: "data" },
    { id: "Algorithms", articles: 19, group: "design" },
    { id: "Security", articles: 18, group: "infra" },
    { id: "SEO & Marketing", articles: 16, group: "other" },
    { id: "Testing & QA", articles: 15, group: "design" },
    { id: "Rust", articles: 14, group: "code" },
    { id: "PHP", articles: 12, group: "code" },
    { id: "Node.js", articles: 10, group: "code" },
    { id: "iOS & Mobile", articles: 10, group: "code" },
    { id: "Misc", articles: 9, group: "other" },
  ];

  const links = [
    { source: "Kafka", target: "Architecture", strength: 3 },
    { source: "Kafka", target: "Data Engineering", strength: 3 },
    { source: "Kafka", target: "Java & Spring", strength: 2 },
    { source: "Kafka", target: "DevOps", strength: 1 },
    { source: "Python", target: "Data Science", strength: 3 },
    { source: "Python", target: "Data Engineering", strength: 2 },
    { source: "Python", target: "LLM & Agents", strength: 2 },
    { source: "Python", target: "Testing & QA", strength: 2 },
    { source: "Python", target: "Web Frontend", strength: 1 },
    { source: "SQL & Databases", target: "Data Engineering", strength: 3 },
    { source: "SQL & Databases", target: "BI & Analytics", strength: 3 },
    { source: "SQL & Databases", target: "Architecture", strength: 2 },
    { source: "SQL & Databases", target: "Python", strength: 1 },
    { source: "DevOps", target: "Linux CLI", strength: 3 },
    { source: "DevOps", target: "Architecture", strength: 2 },
    { source: "DevOps", target: "Security", strength: 2 },
    { source: "DevOps", target: "Kafka", strength: 1 },
    { source: "Architecture", target: "Testing & QA", strength: 2 },
    { source: "Architecture", target: "Algorithms", strength: 1 },
    { source: "Data Science", target: "LLM & Agents", strength: 3 },
    { source: "Data Science", target: "Data Engineering", strength: 2 },
    { source: "Data Science", target: "Algorithms", strength: 2 },
    { source: "Data Science", target: "BI & Analytics", strength: 1 },
    { source: "LLM & Agents", target: "Architecture", strength: 2 },
    { source: "LLM & Agents", target: "Data Engineering", strength: 1 },
    { source: "Web Frontend", target: "Node.js", strength: 2 },
    { source: "Web Frontend", target: "Testing & QA", strength: 1 },
    { source: "Web Frontend", target: "SEO & Marketing", strength: 2 },
    { source: "Java & Spring", target: "Architecture", strength: 3 },
    { source: "Java & Spring", target: "Testing & QA", strength: 1 },
    { source: "Rust", target: "Algorithms", strength: 2 },
    { source: "Rust", target: "Linux CLI", strength: 1 },
    { source: "PHP", target: "SQL & Databases", strength: 2 },
    { source: "PHP", target: "Web Frontend", strength: 1 },
    { source: "Node.js", target: "Architecture", strength: 1 },
    { source: "Security", target: "Linux CLI", strength: 2 },
    { source: "Security", target: "Web Frontend", strength: 1 },
    { source: "iOS & Mobile", target: "Architecture", strength: 1 },
    { source: "BI & Analytics", target: "Data Engineering", strength: 2 },
    { source: "Data Engineering", target: "DevOps", strength: 2 },
  ];

  // Theme detection
  function isDark() {
    const body = document.body.getAttribute("data-md-color-scheme");
    const html = document.documentElement.getAttribute("data-md-color-scheme");
    if (body === "slate" || html === "slate") return true;
    if (body === "default" || html === "default") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function getColors() {
    const dark = isDark();
    return {
      node: {
        data: dark ? "#bb86fc" : "#7c4dff",
        code: dark ? "#03dac6" : "#00bfa5",
        infra: dark ? "#ff7597" : "#ff5252",
        ai: dark ? "#ffd740" : "#ffab00",
        design: dark ? "#82b1ff" : "#448aff",
        other: dark ? "#b0bec5" : "#78909c",
      },
      link: dark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)",
      linkHover: dark ? "rgba(255,255,255,0.25)" : "rgba(0,0,0,0.2)",
      text: dark ? "rgba(255,255,255,0.85)" : "rgba(0,0,0,0.75)",
      textDim: dark ? "rgba(255,255,255,0.4)" : "rgba(0,0,0,0.35)",
      signal: dark ? 0.7 : 0.5,
    };
  }

  // Canvas
  const canvas = document.createElement("canvas");
  const dpr = window.devicePixelRatio || 1;
  container.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  let width, height;
  function resize() {
    width = container.clientWidth;
    height = container.clientHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();

  // Spread nodes across full width using grid-like initial positions
  const cols = 7;
  const rows = Math.ceil(domains.length / cols);
  const padX = 60, padY = 50;
  const cellW = (width - padX * 2) / (cols - 1);
  const cellH = (height - padY * 2) / (rows - 1 || 1);

  const nodes = domains.map((d, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    // Offset odd rows for organic feel
    const offsetX = row % 2 === 1 ? cellW * 0.5 : 0;
    return {
      ...d,
      x: padX + col * cellW + offsetX + (Math.random() - 0.5) * 30,
      y: padY + row * cellH + (Math.random() - 0.5) * 20,
      vx: 0,
      vy: 0,
      radius: Math.sqrt(d.articles) * 2.5 + 7,
      // Gentle drift
      driftPhase: Math.random() * Math.PI * 2,
      driftSpeed: 0.003 + Math.random() * 0.004,
      driftAmpX: 1.5 + Math.random() * 2,
      driftAmpY: 1.0 + Math.random() * 1.5,
      // Hover animation
      hoverAmount: 0, // 0 to 1, smoothly interpolated
    };
  });

  const nodeMap = {};
  nodes.forEach((n) => (nodeMap[n.id] = n));

  const edgeData = links.map((l) => ({
    source: nodeMap[l.source],
    target: nodeMap[l.target],
    strength: l.strength,
  }));

  // Signal particles traveling along edges
  const signals = [];
  function spawnSignal() {
    if (signals.length > 25) return;
    const edge = edgeData[Math.floor(Math.random() * edgeData.length)];
    const reverse = Math.random() > 0.5;
    signals.push({
      edge,
      t: 0,
      speed: 0.0015 + Math.random() * 0.002,
      reverse,
      opacity: 0,
    });
  }

  // Spawn signals periodically
  let signalTimer = 0;

  // Physics - gentler, wider spread
  const config = {
    centerForce: 0.003,
    repulsion: 4500,
    linkForce: 0.003,
    linkDistance: 140,
    damping: 0.92,
  };

  let hoveredNode = null;
  let dragNode = null;
  let time = 0;

  function simulate() {
    // Center gravity (weak)
    nodes.forEach((n) => {
      n.vx += (width / 2 - n.x) * config.centerForce;
      n.vy += (height / 2 - n.y) * config.centerForce;
    });

    // Repulsion
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        let dx = b.x - a.x, dy = b.y - a.y;
        let dist = Math.sqrt(dx * dx + dy * dy) || 1;
        let force = config.repulsion / (dist * dist);
        let fx = (dx / dist) * force, fy = (dy / dist) * force;
        a.vx -= fx; a.vy -= fy;
        b.vx += fx; b.vy += fy;
      }
    }

    // Link springs
    edgeData.forEach((e) => {
      let dx = e.target.x - e.source.x;
      let dy = e.target.y - e.source.y;
      let dist = Math.sqrt(dx * dx + dy * dy) || 1;
      let force = (dist - config.linkDistance) * config.linkForce * e.strength;
      let fx = (dx / dist) * force, fy = (dy / dist) * force;
      e.source.vx += fx; e.source.vy += fy;
      e.target.vx -= fx; e.target.vy -= fy;
    });

    // Update positions
    nodes.forEach((n) => {
      if (n === dragNode) return;
      n.vx *= config.damping;
      n.vy *= config.damping;
      n.x += n.vx;
      n.y += n.vy;

      // Gentle drift (breathing)
      n.driftPhase += n.driftSpeed;
      n.x += Math.sin(n.driftPhase) * n.driftAmpX * 0.15;
      n.y += Math.cos(n.driftPhase * 0.7) * n.driftAmpY * 0.15;

      // Boundary
      const m = n.radius + 10;
      n.x = Math.max(m, Math.min(width - m, n.x));
      n.y = Math.max(m, Math.min(height - m, n.y));

      // Smooth hover interpolation
      const targetHover = n === hoveredNode ? 1 : 0;
      n.hoverAmount += (targetHover - n.hoverAmount) * 0.08;
    });

    // Update signals
    signalTimer++;
    if (signalTimer > 12) { spawnSignal(); signalTimer = 0; }

    for (let i = signals.length - 1; i >= 0; i--) {
      const s = signals[i];
      s.t += s.speed;
      // Fade in/out
      if (s.t < 0.15) s.opacity = s.t / 0.15;
      else if (s.t > 0.85) s.opacity = (1 - s.t) / 0.15;
      else s.opacity = 1;
      if (s.t >= 1) { signals.splice(i, 1); }
    }
  }

  function draw() {
    const colors = getColors();
    time += 0.01;
    ctx.clearRect(0, 0, width, height);

    // Connected set for hover dimming
    let connectedSet = new Set();
    if (hoveredNode) {
      connectedSet.add(hoveredNode.id);
      edgeData.forEach((e) => {
        if (e.source === hoveredNode) connectedSet.add(e.target.id);
        if (e.target === hoveredNode) connectedSet.add(e.source.id);
      });
    }

    // Draw links
    edgeData.forEach((e) => {
      const isHighlighted = hoveredNode && (e.source === hoveredNode || e.target === hoveredNode);
      const dimmed = hoveredNode && !isHighlighted;

      ctx.beginPath();
      ctx.moveTo(e.source.x, e.source.y);
      ctx.lineTo(e.target.x, e.target.y);

      if (dimmed) {
        ctx.strokeStyle = "rgba(128,128,128,0.02)";
        ctx.lineWidth = 0.5;
      } else if (isHighlighted) {
        ctx.strokeStyle = colors.linkHover;
        ctx.lineWidth = 1.5 + e.strength * 0.4;
      } else {
        ctx.strokeStyle = colors.link;
        ctx.lineWidth = 0.7 + e.strength * 0.2;
      }
      ctx.stroke();
    });

    // Draw signal particles
    signals.forEach((s) => {
      const e = s.edge;
      const t = s.reverse ? 1 - s.t : s.t;
      const x = e.source.x + (e.target.x - e.source.x) * t;
      const y = e.source.y + (e.target.y - e.source.y) * t;
      const srcColor = colors.node[e.source.group];
      const tgtColor = colors.node[e.target.group];
      // Use source color for first half, blend to target
      const color = s.t < 0.5 ? srcColor : tgtColor;

      const alpha = s.opacity * colors.signal;

      // Glow
      const grad = ctx.createRadialGradient(x, y, 0, x, y, 6);
      grad.addColorStop(0, color + hex(alpha));
      grad.addColorStop(1, color + "00");
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.arc(x, y, 1.8, 0, Math.PI * 2);
      ctx.fillStyle = color + hex(Math.min(1, alpha * 1.5));
      ctx.fill();
    });

    // Draw nodes
    nodes.forEach((n) => {
      const isConnected = connectedSet.has(n.id);
      const dimmed = hoveredNode && !isConnected;
      const h = n.hoverAmount;
      const baseColor = colors.node[n.group];

      // Breathing pulse
      const breath = 1 + Math.sin(n.driftPhase * 1.2) * 0.025;
      const hoverScale = 1 + h * 0.15;
      const r = n.radius * breath * hoverScale;

      // Outer glow on hover (smooth)
      if (h > 0.01) {
        const glowR = r + 8 + h * 8;
        const grad = ctx.createRadialGradient(n.x, n.y, r * 0.8, n.x, n.y, glowR);
        grad.addColorStop(0, baseColor + hex(h * 0.3));
        grad.addColorStop(1, baseColor + "00");
        ctx.beginPath();
        ctx.arc(n.x, n.y, glowR, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.fill();
      }

      // Node body
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      const bodyAlpha = dimmed ? 0.2 : 0.7 + h * 0.3;
      ctx.fillStyle = baseColor + hex(bodyAlpha);
      ctx.fill();

      // Border
      ctx.strokeStyle = dimmed ? baseColor + "15" : baseColor + hex(0.8 + h * 0.2);
      ctx.lineWidth = 1 + h * 0.5;
      ctx.stroke();

      // Article count
      if (r > 10) {
        const fs = Math.max(9, r * 0.6 + h * 2);
        ctx.font = `700 ${fs}px Inter, system-ui, sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = dimmed ? "rgba(255,255,255,0.08)" : "rgba(255,255,255," + (0.85 + h * 0.15) + ")";
        ctx.fillText(n.articles, n.x, n.y);
      }

      // Label below
      const labelFs = 9 + h * 2;
      ctx.font = `${500 + h * 200} ${labelFs}px Inter, system-ui, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = dimmed ? colors.textDim + "40" : h > 0.5 ? colors.text : colors.textDim;
      ctx.fillText(n.id, n.x, n.y + r + 4);
    });

    // Tooltip
    if (hoveredNode && hoveredNode.hoverAmount > 0.5) {
      const n = hoveredNode;
      const connCount = edgeData.filter(
        (e) => e.source === n || e.target === n
      ).length;
      const tip = `${n.articles} articles  |  ${connCount} connections`;
      ctx.font = "500 11px Inter, system-ui, sans-serif";
      const tw = ctx.measureText(tip).width;
      const tx = Math.min(Math.max(n.x, tw / 2 + 16), width - tw / 2 - 16);
      const ty = n.y - n.radius * (1 + n.hoverAmount * 0.15) - 24;

      const alpha = (n.hoverAmount - 0.5) * 2; // fade in after 50%
      ctx.globalAlpha = alpha;

      ctx.fillStyle = isDark() ? "rgba(30,30,40,0.92)" : "rgba(255,255,255,0.95)";
      ctx.strokeStyle = isDark() ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)";
      ctx.lineWidth = 1;
      roundRect(ctx, tx - tw / 2 - 10, ty - 11, tw + 20, 24, 8);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = isDark() ? "rgba(255,255,255,0.9)" : "rgba(0,0,0,0.8)";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(tip, tx, ty + 1);

      ctx.globalAlpha = 1;
    }
  }

  function hex(alpha) {
    return Math.round(Math.max(0, Math.min(1, alpha)) * 255).toString(16).padStart(2, "0");
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r);
    ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r);
    ctx.lineTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.closePath();
  }

  function getNodeAt(x, y) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const dx = x - n.x, dy = y - n.y;
      if (dx * dx + dy * dy < (n.radius + 6) * (n.radius + 6)) return n;
    }
    return null;
  }

  // Mouse interaction
  canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    if (dragNode) {
      dragNode.x = mx;
      dragNode.y = my;
      dragNode.vx = 0;
      dragNode.vy = 0;
      return;
    }
    const node = getNodeAt(mx, my);
    if (node !== hoveredNode) {
      hoveredNode = node;
      canvas.style.cursor = node ? "pointer" : "default";
    }
  });

  canvas.addEventListener("mousedown", (e) => {
    const rect = canvas.getBoundingClientRect();
    const node = getNodeAt(e.clientX - rect.left, e.clientY - rect.top);
    if (node) {
      dragNode = node;
      canvas.style.cursor = "grabbing";
    }
  });

  canvas.addEventListener("mouseup", () => {
    dragNode = null;
    canvas.style.cursor = hoveredNode ? "pointer" : "default";
  });

  canvas.addEventListener("mouseleave", () => {
    hoveredNode = null;
    dragNode = null;
    canvas.style.cursor = "default";
  });

  // Animation loop
  function frame() {
    simulate();
    draw();
    requestAnimationFrame(frame);
  }
  frame();

  // Resize
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 100);
  });
})();
