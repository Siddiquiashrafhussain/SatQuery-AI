export default function EvidencePanel() {
    return (
      <div className="glass-panel p-4 absolute bottom-4 left-4 z-10 max-w-sm border-t-2 border-t-purple-500 shadow-2xl">
        <h3 className="text-xs font-semibold text-purple-400 tracking-wider mb-2">VISUAL EVIDENCE</h3>
        <p className="text-sm text-gray-300">
            Bounding boxes and segmentation masks overlayed on the map correspond to the detected features.
        </p>
      </div>
    );
  }
