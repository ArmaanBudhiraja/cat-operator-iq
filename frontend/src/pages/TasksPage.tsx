import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { TaskItem } from '../types';
import { SkeletonCard, ErrorState, EmptyState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Drawer } from '../components/ui/Drawer';
import { Play, Check } from 'lucide-react';

export const TasksPage: React.FC = () => {
  const { role, activeOperatorId } = useRole();
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [selectedTask, setSelectedTask] = useState<TaskItem | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTasks(filterStatus || undefined, role === 'Operator' ? activeOperatorId : undefined);
      setTasks(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchDetailAndOpen = async (taskId: string) => {
    try {
      const detail = await api.getTaskDetail(taskId);
      setSelectedTask(detail);
      setDrawerOpen(true);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadTasks();
  }, [filterStatus, activeOperatorId, role]);

  const handleUpdateStatus = async (taskId: string, newStatus: string) => {
    setActionLoading(true);
    try {
      await api.updateTaskStatus(taskId, newStatus);
      const detail = await api.getTaskDetail(taskId);
      setSelectedTask(detail);
      const updated = await api.getTasks(filterStatus || undefined, role === 'Operator' ? activeOperatorId : undefined);
      setTasks(updated);
    } catch (err) {
      console.error(err);
    } finally {
      setActionLoading(false);
    }
  };

  const scheduledCount = tasks.filter((t) => t.status === 'Scheduled').length;
  const activeCount = tasks.filter((t) => t.status === 'In Progress').length;
  const completedCount = tasks.filter((t) => t.status === 'Completed').length;

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            Today's tasks
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            {tasks.length} total · {scheduledCount} scheduled · {activeCount} active · {completedCount} completed
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 p-0.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] text-xs">
          {['', 'Scheduled', 'In Progress', 'Completed'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1 rounded-[3px] text-xs transition-colors ${
                filterStatus === st
                  ? 'bg-[#111111] text-[#FFFFFF] font-medium shadow-xs'
                  : 'text-[#525252] hover:text-[#171717]'
              }`}
            >
              {st || 'All tasks'}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <SkeletonCard rows={6} />
      ) : error ? (
        <ErrorState error={error} onRetry={loadTasks} />
      ) : tasks.length === 0 ? (
        <EmptyState
          title="No tasks in queue"
          message="No operational tasks matched the selected filter criteria."
          actionLabel="Show all tasks"
          onAction={() => setFilterStatus('')}
        />
      ) : (
        /* Operational Table */
        <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] overflow-x-auto shadow-xs">
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="bg-[#FAFAFA] border-b border-[#E5E5E5] text-xs text-[#525252] font-medium">
                <th className="py-2.5 px-4 font-medium">Task</th>
                <th className="py-2.5 px-4 font-medium">Type</th>
                <th className="py-2.5 px-4 font-medium">Machine</th>
                <th className="py-2.5 px-4 font-medium text-right">Predicted</th>
                <th className="py-2.5 px-4 font-medium text-right">Estimated</th>
                <th className="py-2.5 px-4 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E5E5] text-[13px]">
              {tasks.map((task) => {
                const isInProg = task.status === 'In Progress';
                const isDone = task.status === 'Completed';
                const badgeVariant = isInProg ? 'warning' : isDone ? 'safe' : 'neutral';

                return (
                  <tr
                    key={task.task_id}
                    onClick={() => fetchDetailAndOpen(task.task_id)}
                    className="cursor-pointer hover:bg-[#F5F5F5] transition-colors"
                  >
                    <td className="py-3 px-4 text-[#737373] font-mono text-xs">
                      {task.task_id}
                    </td>

                    <td className="py-3 px-4 text-[#171717] font-medium">
                      {task.task_type}
                      <span className="block text-xs text-[#737373] font-normal mt-0.5">
                        {task.location}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-[#171717] font-mono text-xs">
                      {task.machine_id}
                    </td>

                    <td className="py-3 px-4 text-right font-medium text-[#171717] tabular-nums">
                      {task.predicted_time_min?.toFixed(0) || 54} min
                    </td>

                    <td className="py-3 px-4 text-right text-[#737373] tabular-nums">
                      {task.estimated_time_min} min
                    </td>

                    <td className="py-3 px-4 text-right">
                      <Badge variant={badgeVariant} size="sm">
                        {task.status}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Task Detail Drawer */}
      <Drawer
        isOpen={drawerOpen && !!selectedTask}
        onClose={() => setDrawerOpen(false)}
        title={selectedTask?.task_type || 'Task detail'}
        subtitle={`${selectedTask?.task_id} · ${selectedTask?.machine_id}`}
        width="max-w-[460px]"
      >
        {selectedTask && (
          <div className="space-y-5 text-xs font-sans">
            {/* Status & Actions */}
            <div className="flex items-center justify-between p-3.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px]">
              <div className="flex items-center gap-2">
                <span className="text-[#737373] text-xs">Status:</span>
                <Badge
                  variant={
                    selectedTask.status === 'In Progress'
                      ? 'warning'
                      : selectedTask.status === 'Completed'
                      ? 'safe'
                      : 'neutral'
                  }
                >
                  {selectedTask.status}
                </Badge>
              </div>

              <div className="flex items-center gap-2">
                {selectedTask.status === 'Scheduled' && (
                  <Button
                    variant="primary"
                    size="sm"
                    loading={actionLoading}
                    onClick={() => handleUpdateStatus(selectedTask.task_id, 'In Progress')}
                    icon={<Play className="w-3 h-3 text-current" />}
                  >
                    Start task
                  </Button>
                )}
                {selectedTask.status === 'In Progress' && (
                  <Button
                    variant="secondary"
                    size="sm"
                    loading={actionLoading}
                    onClick={() => handleUpdateStatus(selectedTask.task_id, 'Completed')}
                    icon={<Check className="w-3 h-3 text-current" />}
                  >
                    Mark completed
                  </Button>
                )}
              </div>
            </div>

            {/* Task Overview Details */}
            <div className="space-y-2.5 py-3 border-y border-[#E5E5E5]">
              <div className="flex justify-between">
                <span className="text-[#737373]">Machine</span>
                <span className="text-[#171717] font-medium font-mono">{selectedTask.machine_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Operator</span>
                <span className="text-[#171717] font-mono">{selectedTask.operator_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Estimated</span>
                <span className="text-[#171717] tabular-nums">{selectedTask.estimated_time_min} min</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Predicted</span>
                <span className="text-[#171717] font-semibold tabular-nums">
                  {selectedTask.prediction_details?.predicted_time_min || selectedTask.predicted_time_min || 54} min
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Confidence interval</span>
                <span className="text-[#525252] tabular-nums">±7 min (90% CI)</span>
              </div>
            </div>

            {/* Prediction Factors */}
            <div className="space-y-2.5">
              <div className="text-xs font-semibold text-[#171717]">
                Prediction factors
              </div>

              <div className="space-y-1.5">
                <div className="p-2.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px] flex items-center justify-between">
                  <span className="text-[#171717]">Weather impact</span>
                  <span className="text-[#171717] font-semibold tabular-nums">+4 min</span>
                </div>

                <div className="p-2.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px] flex items-center justify-between">
                  <span className="text-[#171717]">Operator experience</span>
                  <span className="text-[#525252] font-semibold tabular-nums">-6 min</span>
                </div>

                <div className="p-2.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px] flex items-center justify-between">
                  <span className="text-[#171717]">Machine age & hours</span>
                  <span className="text-[#171717] font-semibold tabular-nums">+2 min</span>
                </div>

                <div className="p-2.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px] flex items-center justify-between">
                  <span className="text-[#171717]">Planned load cycles</span>
                  <span className="text-[#171717] font-semibold tabular-nums">+3 min</span>
                </div>
              </div>
            </div>

            {/* Model note */}
            <div className="pt-2 text-xs text-[#737373] leading-relaxed">
              Model: GradientBoostingRegressor · Trained on 2,000 historical Caterpillar operational task cycles.
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
};
