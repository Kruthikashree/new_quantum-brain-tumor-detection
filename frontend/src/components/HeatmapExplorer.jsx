import { useRef, useState, useEffect, useCallback } from "react";
import "./HeatmapExplorer.css";

function classifyPixel(r, g, b) {
  const brightness = (r + g + b) / 3;

  if (brightness < 35 && Math.abs(r - b) < 15) {
    return { label: "Background", detail: "No AI attention in this area" };
  }

  const warm = r - b;
  const greenish = g - Math.min(r, b);

  if (warm > 20 && r >= g) {
    return { label: "High influence", detail: "Strongly influenced this prediction" };
  }
  if (greenish > 10 && g >= b) {
    return { label: "Moderate influence", detail: "Partially influenced this prediction" };
  }
  if (b - r > 10) {
    return { label: "Low influence", detail: "Minimal effect on this prediction" };
  }
  return { label: "Brain tissue", detail: "Outside the highlighted attention regions" };
}

function HeatmapExplorer({ src, alt }) {
  const imgRef = useRef(null);
  const canvasRef = useRef(null);
  const [tooltip, setTooltip] = useState(null);
  const [ready, setReady] = useState(false);

  const drawToCanvas = useCallback(() => {
    const img = imgRef.current;
    const canvas = canvasRef.current;
    if (!img || !canvas || !img.naturalWidth) return;
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    setReady(true);
  }, []);

  useEffect(() => {
    setReady(false);
    // Handles the case where the image is already cached/loaded
    // before this effect runs, so the onLoad event never fires.
    const img = imgRef.current;
    if (img && img.complete && img.naturalWidth) {
      drawToCanvas();
    }
  }, [src, drawToCanvas]);

  const handleMove = (e) => {
    if (!ready) {
      drawToCanvas(); // last-resort retry
      if (!ready) return;
    }
    const img = imgRef.current;
    const canvas = canvasRef.current;
    if (!img || !canvas) return;
    const rect = img.getBoundingClientRect();

    const xRatio = (e.clientX - rect.left) / rect.width;
    const yRatio = (e.clientY - rect.top) / rect.height;
    if (xRatio < 0 || xRatio > 1 || yRatio < 0 || yRatio > 1) {
      setTooltip(null);
      return;
    }

    const px = Math.min(canvas.width - 1, Math.max(0, Math.floor(xRatio * canvas.width)));
    const py = Math.min(canvas.height - 1, Math.max(0, Math.floor(yRatio * canvas.height)));

    try {
      const data = canvas.getContext("2d").getImageData(px, py, 1, 1).data;
      const info = classifyPixel(data[0], data[1], data[2]);
      setTooltip({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        ...info,
      });
    } catch (err) {
      setTooltip(null);
    }
  };

  return (
    <div className="heatmap-explorer">
      <img
        ref={imgRef}
        src={src}
        alt={alt}
        onLoad={drawToCanvas}
        onMouseMove={handleMove}
        onMouseLeave={() => setTooltip(null)}
        className="heatmap-explorer-img"
      />
      <canvas ref={canvasRef} style={{ display: "none" }} />

      {tooltip && (
        <div
          className="heatmap-hover-tooltip"
          style={{ left: tooltip.x + 16, top: tooltip.y }}
        >
          <b>{tooltip.label}</b>
          <span>{tooltip.detail}</span>
        </div>
      )}

      <p className="heatmap-hint">Move your cursor over the image to inspect each region</p>
    </div>
  );
}

export default HeatmapExplorer;