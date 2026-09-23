import React, { useState } from 'react';
import { TrainingCourse } from '../types';
import { api } from '../services/api';
import { X, Check, AlertCircle } from 'lucide-react';
import { Button } from './ui/Button';
import { Badge } from './ui/Badge';

interface QuizModalProps {
  course: TrainingCourse;
  operatorId: string;
  onClose: () => void;
  onQuizCompleted: () => void;
}

export const QuizModal: React.FC<QuizModalProps> = ({
  course,
  operatorId,
  onClose,
  onQuizCompleted,
}) => {
  const questions = course.quiz_questions || [];
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any | null>(null);

  const handleSelectOption = (questionId: number, optionIdx: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionIdx }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await api.submitQuiz(course.course_id, operatorId, answers);
      setResult(res);
      onQuizCompleted();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const isComplete = questions.length > 0 && Object.keys(answers).length === questions.length;

  return (
    <div className="fixed inset-0 z-50 bg-[#000000]/40 backdrop-blur-xs flex items-center justify-center p-4 select-none">
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] max-w-xl w-full p-6 relative max-h-[90vh] overflow-y-auto shadow-lg">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-[#737373] hover:text-[#171717] p-1 transition-colors rounded-[4px] hover:bg-[#F5F5F5]"
          aria-label="Close modal"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="mb-4 pb-3 border-b border-[#E5E5E5]">
          <Badge variant="warning" size="sm">
            Evaluation
          </Badge>
          <h3 className="text-base font-semibold text-[#171717] mt-1.5 font-sans">
            {course.title}
          </h3>
          <p className="text-xs text-[#525252] mt-0.5 font-sans">
            {course.description}
          </p>
        </div>

        {result ? (
          <div className="my-5 text-center py-6 px-4 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[6px] space-y-3 font-sans">
            <div className="w-10 h-10 rounded-full bg-[#FFFFFF] border border-[#E5E5E5] mx-auto flex items-center justify-center">
              {result.passed ? (
                <Check className="w-5 h-5 text-[#171717]" />
              ) : (
                <AlertCircle className="w-5 h-5 text-[#737373]" />
              )}
            </div>

            <h4 className="text-sm font-semibold text-[#171717]">
              {result.passed ? 'Certification Competency Achieved' : 'Evaluation Incomplete'}
            </h4>
            <div className="text-4xl font-semibold text-[#171717] tabular-nums">
              {result.score_pct}%
            </div>
            <p className="text-xs text-[#525252] max-w-xs mx-auto font-sans leading-relaxed">
              {result.message} ({result.correct_answers} of {result.total_questions} correct)
            </p>

            <div className="pt-2">
              <Button variant="primary" size="md" onClick={onClose}>
                Return to modules
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4 my-3 font-sans">
            {questions.map((q, qIndex) => (
              <div key={q.id} className="p-3.5 rounded-[6px] bg-[#FAFAFA] border border-[#E5E5E5]">
                <div className="text-xs font-semibold text-[#171717] mb-2.5 flex items-start gap-2">
                  <span className="text-[#737373]">Q{qIndex + 1}.</span>
                  <span>{q.question}</span>
                </div>

                <div className="space-y-1.5 mt-2">
                  {q.options.map((opt, optIndex) => {
                    const isSelected = answers[q.id] === optIndex;
                    return (
                      <button
                        key={optIndex}
                        type="button"
                        onClick={() => handleSelectOption(q.id, optIndex)}
                        className={`w-full text-left p-2.5 rounded-[4px] text-xs transition-colors border flex items-center justify-between font-sans ${
                          isSelected
                            ? 'bg-[#FFFFFF] border-[#111111] text-[#171717] font-medium shadow-xs'
                            : 'bg-[#FFFFFF] border-[#E5E5E5] text-[#525252] hover:border-[#D4D4D4] hover:text-[#171717]'
                        }`}
                      >
                        <span>{opt}</span>
                        <div
                          className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center shrink-0 ml-3 ${
                            isSelected ? 'border-[#111111] bg-[#111111]' : 'border-[#D4D4D4]'
                          }`}
                        >
                          {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-[#FFFFFF]"></div>}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}

            <div className="flex items-center justify-between pt-3 border-t border-[#E5E5E5] text-xs">
              <span className="text-[#737373]">
                {Object.keys(answers).length} of {questions.length} answered
              </span>

              <Button
                variant="primary"
                size="md"
                disabled={!isComplete || submitting}
                loading={submitting}
                onClick={handleSubmit}
              >
                Submit evaluation
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
