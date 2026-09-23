import React, { useState } from 'react';
import { api } from '../services/api';
import { X } from 'lucide-react';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

interface IncidentModalProps {
  onClose: () => void;
  onSuccess: () => void;
  defaultMachineId?: string;
  defaultOperatorId?: string;
}

export const IncidentModal: React.FC<IncidentModalProps> = ({
  onClose,
  onSuccess,
  defaultMachineId = 'EXC001',
  defaultOperatorId = 'OP001',
}) => {
  const [machineId, setMachineId] = useState(defaultMachineId);
  const [operatorId, setOperatorId] = useState(defaultOperatorId);
  const [incidentType, setIncidentType] = useState('Proximity Hazard');
  const [severity, setSeverity] = useState('High');
  const [location, setLocation] = useState('Site Alpha - Sector 4 Foundation');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;

    setSubmitting(true);
    try {
      await api.createIncident({
        machine_id: machineId,
        operator_id: operatorId,
        incident_type: incidentType,
        severity,
        location,
        description,
      });
      onSuccess();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-[#000000]/40 backdrop-blur-xs flex items-center justify-center p-4 select-none">
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] max-w-lg w-full p-6 relative shadow-lg">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-[#737373] hover:text-[#171717] p-1 transition-colors rounded-[4px] hover:bg-[#F5F5F5]"
          aria-label="Close modal"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="mb-4 pb-3 border-b border-[#E5E5E5]">
          <Badge variant="warning" size="sm">
            Formal record
          </Badge>
          <h3 className="text-base font-semibold text-[#171717] mt-1.5 font-sans">
            Log safety incursion
          </h3>
          <p className="text-xs text-[#525252] mt-0.5 font-sans">
            Formal entry for safety audit, root-cause investigation, and shift sign-off.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3.5 text-xs font-sans">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
                Machine ID
              </label>
              <input
                type="text"
                value={machineId}
                onChange={(e) => setMachineId(e.target.value)}
                className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] placeholder-[#737373] focus:border-[#737373] focus:outline-none font-mono"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
                Operator ID
              </label>
              <input
                type="text"
                value={operatorId}
                onChange={(e) => setOperatorId(e.target.value)}
                className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] placeholder-[#737373] focus:border-[#737373] focus:outline-none font-mono"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
                Category
              </label>
              <select
                value={incidentType}
                onChange={(e) => setIncidentType(e.target.value)}
                className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] focus:border-[#737373] focus:outline-none cursor-pointer"
              >
                <option value="Proximity Hazard">Proximity Hazard</option>
                <option value="Seatbelt Violation">Seatbelt Violation</option>
                <option value="Mechanical Anomaly">Mechanical Anomaly</option>
                <option value="Overheating">Overheating</option>
                <option value="Excessive Idling">Excessive Idling</option>
                <option value="Fatigue">Operator Fatigue</option>
                <option value="Other">Other Operational Incursion</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
                Severity
              </label>
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
                className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] focus:border-[#737373] focus:outline-none cursor-pointer"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
              Jobsite location
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] placeholder-[#737373] focus:border-[#737373] focus:outline-none font-sans"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-[#525252] mb-1 font-sans">
              Description & context
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Detail observations, ground conditions, personnel involved, and immediate corrective steps..."
              rows={3}
              className="w-full bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2 text-xs text-[#171717] placeholder-[#737373] focus:border-[#737373] focus:outline-none resize-none font-sans"
              required
            />
          </div>

          <div className="flex justify-end gap-2.5 pt-3 border-t border-[#E5E5E5]">
            <Button type="button" variant="secondary" size="md" onClick={onClose}>
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              size="md"
              loading={submitting}
            >
              Log incident
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
