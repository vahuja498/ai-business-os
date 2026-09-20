"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TasksPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getTasks();
        setTasks(res);
      } catch (err: any) {
        alert(`Error: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Execution Tasks</h1>
        <p className="text-sm text-slate-400">Decomposed tasks assigned to specialist agents with retry policies and audit tracking.</p>
      </div>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No tasks found.
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <div key={task.id} className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-white">{task.title}</p>
                <p className="text-xs text-slate-400 mt-0.5">
                  Business: <span className="font-mono text-indigo-400">{task.business_id?.substring(0, 8)}...</span> | Created: {new Date(task.created_at).toLocaleString()}
                </p>
              </div>
              <span
                className={`text-xs px-2.5 py-1 rounded font-mono font-medium ${
                  task.status === "COMPLETED"
                    ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                    : task.status === "PENDING_APPROVAL"
                    ? "bg-amber-950 text-amber-300 border border-amber-800"
                    : "bg-slate-800 text-slate-300 border border-slate-700"
                }`}
              >
                {task.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
