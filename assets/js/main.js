/* The Economic Review at W&M — all JavaScript is progressive enhancement.
   Every piece of content renders server-side; this file only (1) powers the
   theme toggle, (2) keeps deadline displays fresh between rebuilds, and
   (3) adds copy buttons to citation blocks. Keep it dependency-free and
   under 5 KB. */
(function () {
  "use strict";
  var doc = document.documentElement;

  /* ── Theme toggle ─────────────────────────────────────────────────── */
  var btn = document.querySelector(".theme-toggle");
  if (btn) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");
    var current = function () {
      return doc.getAttribute("data-theme") || (media.matches ? "dark" : "light");
    };
    var paint = function () {
      var dark = current() === "dark";
      btn.textContent = dark ? "Light mode" : "Dark mode";
      btn.setAttribute("aria-pressed", String(dark));
    };
    btn.hidden = false;
    paint();
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      doc.setAttribute("data-theme", next);
      try { localStorage.setItem("wmer-theme", next); } catch (e) {}
      paint();
    });
    media.addEventListener("change", paint);
  }

  /* ── Stale-date protection ────────────────────────────────────────────
     GitHub Pages only rebuilds on push, so the server-rendered "next
     deadline" can go stale. The full calendar is embedded as JSON; at page
     view we re-select the next future deadline and dim past timeline steps.
     A date counts as past 30h after midnight UTC on that date, which covers
     end-of-day US Eastern without shipping a timezone table. */
  var dataEl = document.getElementById("wmer-dates");
  if (dataEl) {
    var dates = [];
    try { dates = JSON.parse(dataEl.textContent); } catch (e) {}
    var passed = function (iso) {
      var t = Date.parse(iso);
      return !isNaN(t) && Date.now() > t + 30 * 3600 * 1000;
    };
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-next-deadline]"),
      function (el) {
        var track = el.getAttribute("data-next-deadline");
        var next = dates.filter(function (d) {
          return d.type === "deadline" && d.track === track && !passed(d.date);
        })[0];
        var time = el.querySelector("time");
        if (next && time) {
          time.textContent = next.display;
          time.setAttribute("datetime", next.datetime);
        } else if (!next) {
          el.textContent = el.getAttribute("data-fallback") || el.textContent;
        }
      }
    );
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-date]"),
      function (li) {
        if (passed(li.getAttribute("data-date"))) li.classList.add("is-past");
      }
    );
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-hide-past]"),
      function (el) {
        if (passed(el.getAttribute("data-hide-past"))) el.hidden = true;
      }
    );
  }

  /* ── Citation copy buttons (injected: no dead buttons without JS) ──── */
  if (navigator.clipboard) {
    Array.prototype.forEach.call(
      document.querySelectorAll(".citation"),
      function (c) {
        var p = c.querySelector("p");
        if (!p) return;
        var b = document.createElement("button");
        b.type = "button";
        b.className = "copy-btn";
        b.textContent = "Copy";
        b.addEventListener("click", function () {
          navigator.clipboard.writeText(p.textContent.trim()).then(function () {
            b.textContent = "Copied";
            setTimeout(function () { b.textContent = "Copy"; }, 1600);
          });
        });
        c.appendChild(b);
      }
    );
  }
})();
