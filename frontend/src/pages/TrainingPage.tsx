import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { TrainingCourse } from '../types';
import { QuizModal } from '../components/QuizModal';
import { SkeletonCard, ErrorState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { ProgressBar } from '../components/ui/ProgressBar';
import { SectionHeader } from '../components/ui/SectionHeader';
import { ArrowRight, Check } from 'lucide-react';

export const TrainingPage: React.FC = () => {
  const { activeOperatorId } = useRole();
  const [courses, setCourses] = useState<TrainingCourse[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [selectedCourseForQuiz, setSelectedCourseForQuiz] = useState<TrainingCourse | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTraining = async (showSkeleton = true) => {
    try {
      if (showSkeleton) setLoading(true);
      setError(null);
      const res = await api.getTraining(activeOperatorId);
      setCourses(res.courses);
      setRecommendations(res.recommendations);
    } catch (err: any) {
      setError(err.message || 'Failed to load training courses');
    } finally {
      if (showSkeleton) setLoading(false);
    }
  };

  useEffect(() => {
    loadTraining();
  }, [activeOperatorId]);

  const categories = [
    '',
    'Safety',
    'Machine Operation',
    'Fuel Efficiency',
    'Maintenance Awareness',
    'Emergency Procedures'
  ];

  const filteredCourses = filterCategory
    ? courses.filter((c) => c.category === filterCategory)
    : courses;

  const completedCourses = courses.filter((c) => c.completion_status === 'Completed').length;
  const overallProgress = courses.length > 0 ? Math.round((completedCourses / courses.length) * 100) : 0;

  const primaryRec = recommendations[0] || {
    title: 'Proximity safety',
    duration: '8 min',
    reason: 'Recommended based on recent safety events.',
    recommendation: 'Complete 360-degree LiDAR and visual blind spot perimeter procedures.',
  };

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            Training
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            Recommended learning · Operator {activeOperatorId}
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 p-0.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] text-xs">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={`px-3 py-1 rounded-[3px] text-xs transition-colors ${
                filterCategory === cat
                  ? 'bg-[#111111] text-[#FFFFFF] font-medium shadow-xs'
                  : 'text-[#525252] hover:text-[#171717]'
              }`}
            >
              {cat || 'All modules'}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <SkeletonCard rows={5} />
      ) : error ? (
        <ErrorState error={error} onRetry={loadTraining} />
      ) : (
        <div className="space-y-6">
          {/* Primary Recommendation */}
          <div className="p-5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2">
                <Badge variant="warning" size="sm">Recommended</Badge>
                <span className="text-xs text-[#737373]">{primaryRec.duration || '8 min'}</span>
              </div>

              <h2 className="text-lg font-semibold text-[#171717]">
                {primaryRec.title || 'Proximity Safety'}
              </h2>

              <p className="text-xs text-[#525252] max-w-xl leading-relaxed">
                {primaryRec.recommendation}
              </p>

              <div className="text-xs text-[#737373]">
                {primaryRec.reason || 'Recommended based on recent safety events.'}
              </div>
            </div>

            <div className="shrink-0">
              <Button
                variant="primary"
                size="md"
                onClick={() => {
                  const matched = courses.find((c) =>
                    c.title.toLowerCase().includes('proximity') || c.category === 'Safety'
                  );
                  if (matched) setSelectedCourseForQuiz(matched);
                  else if (courses.length > 0) setSelectedCourseForQuiz(courses[0]);
                }}
                icon={<ArrowRight className="w-4 h-4 text-current" />}
              >
                Start training
              </Button>
            </div>
          </div>

          {/* Progress Overview Bar */}
          <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-4 shadow-xs space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-[#525252]">Curriculum progress</span>
              <span className="text-[#171717] tabular-nums font-semibold">Completed {overallProgress}%</span>
            </div>
            <ProgressBar value={overallProgress} size="xs" />
            <div className="flex justify-between text-xs text-[#737373] pt-0.5">
              <span>{completedCourses} of {courses.length} certified modules</span>
              <span>Operator ID: {activeOperatorId}</span>
            </div>
          </div>

          {/* Assigned Modules Grid */}
          <div className="space-y-3">
            <SectionHeader
              title="Assigned modules"
              count={filteredCourses.length}
              description="Standardized machine and jobsite procedure certifications"
            />

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              {filteredCourses.map((course) => {
                const isCompleted = course.completion_status === 'Completed';

                return (
                  <div
                    key={course.course_id}
                    className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs flex flex-col justify-between space-y-3 hover:border-[#D4D4D4] transition-colors"
                  >
                    <div>
                      <div className="flex items-center justify-between text-[#737373] text-xs mb-1.5">
                        <span>{course.category}</span>
                        <span>{course.duration_min} min</span>
                      </div>

                      <h3 className="text-sm font-semibold text-[#171717]">
                        {course.title}
                      </h3>

                      <p className="text-xs text-[#525252] mt-1 line-clamp-2 leading-relaxed">
                        {course.description}
                      </p>
                    </div>

                    <div className="pt-2.5 border-t border-[#E5E5E5] flex items-center justify-between">
                      <div>
                        {isCompleted ? (
                          <span className="text-[#171717] text-xs font-medium flex items-center gap-1">
                            <Check className="w-3.5 h-3.5 text-[#171717]" />
                            {course.score}% Certified
                          </span>
                        ) : (
                          <span className="text-[#737373] text-xs">
                            Pending
                          </span>
                        )}
                      </div>

                      <button
                        onClick={() => setSelectedCourseForQuiz(course)}
                        className="text-[#171717] hover:underline text-xs font-medium flex items-center gap-1 transition-colors"
                      >
                        <span>{isCompleted ? 'Review' : 'Start'}</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Quiz Modal */}
      {selectedCourseForQuiz && (
        <QuizModal
          course={selectedCourseForQuiz}
          operatorId={activeOperatorId}
          onClose={() => setSelectedCourseForQuiz(null)}
          onQuizCompleted={() => loadTraining(false)}
        />
      )}
    </div>
  );
};
