/**
 * dashboard.js
 * ---------------------------------------
 * SOC / SIEM Dashboard Controller
 * - KPI counter animation
 * - Sidebar active state
 * - Smooth panel/card animations
 * - Auto refresh hook (optional)
 * ---------------------------------------
 */

document.addEventListener("DOMContentLoaded", () => {

  /* =====================================================
     KPI COUNTER ANIMATION
     (Used for Total Scans, High Risk, Alerts, etc.)
  ===================================================== */
  const counters = document.querySelectorAll("[data-count]");

  counters.forEach(counter => {
    const target = Number(counter.dataset.count);
    let current = 0;

    const increment = Math.max(1, Math.floor(target / 40));

    const animate = () => {
      current += increment;
      if (current >= target) {
        counter.textContent = target;
      } else {
        counter.textContent = current;
        requestAnimationFrame(animate);
      }
    };

    animate();
  });


  /* =====================================================
     SIDEBAR ACTIVE LINK HIGHLIGHT
  ===================================================== */
  const sidebarLinks = document.querySelectorAll(".sidebar a");
  const currentPath = window.location.pathname;

  sidebarLinks.forEach(link => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });


  /* =====================================================
     FADE & SLIDE-IN ANIMATION FOR CARDS
  ===================================================== */
  const animatedElements = document.querySelectorAll(
    ".card, .panel, .analysis-box"
  );

  animatedElements.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(12px)";

    setTimeout(() => {
      el.style.transition = "all 0.45s ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, index * 80);
  });


  /* =====================================================
     CRITICAL ALERT VISUAL HIGHLIGHT
     (Auto-detect critical badges)
  ===================================================== */
  const criticalBadges = document.querySelectorAll(".badge.critical");

  criticalBadges.forEach(badge => {
    badge.style.boxShadow = "0 0 12px rgba(231,76,60,0.7)";
  });


  /* =====================================================
     OPTIONAL AUTO-REFRESH (FOR LIVE SOC)
     Enable only when real-time feeds exist
  ===================================================== */
  /*
  setInterval(() => {
    window.location.reload();
  }, 300000); // 5 minutes
  */


  /* =====================================================
     DEV CONFIRMATION
  ===================================================== */
  console.log("✅ SOC Dashboard JS loaded successfully");

});
