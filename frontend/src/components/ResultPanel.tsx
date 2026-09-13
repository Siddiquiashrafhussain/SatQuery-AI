export default function ResultPanel() {
    return (
      <div className="glass-panel p-6 flex flex-col gap-4 border-t-4 border-t-sat-accent bg-sat-accent/5">
        <h3 className="text-sm font-semibold text-sat-accent tracking-wider">ANSWER</h3>
        <div className="text-gray-200 leading-relaxed">
          <p>
            Based on the analysis of the optical imagery, there are <strong>3 large industrial buildings</strong> 
            and <strong>15 vehicles</strong> visible near the main access road in the northeastern quadrant.
          </p>
        </div>
      </div>
    );
  }
