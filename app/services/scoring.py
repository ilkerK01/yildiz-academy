from __future__ import annotations

from app.models import LabProgress, LabStep, StepProgress


def step_award(step: LabStep, hints_used: int) -> int:
    penalty = sum(h.penalty for h in step.hints[:hints_used])
    return max(0, step.points - penalty)


def lab_award(lab_progress: LabProgress, step_rows: list[StepProgress]) -> int:
    if lab_progress.solution_seen:
        return 0
    return sum(row.earned_points for row in step_rows if row.solved)


def lab_potential(step_rows: list[StepProgress], steps: list[LabStep]) -> int:
    used = {row.step_id: row.hints_used for row in step_rows}
    return sum(step_award(step, used.get(step.id, 0)) for step in steps)
