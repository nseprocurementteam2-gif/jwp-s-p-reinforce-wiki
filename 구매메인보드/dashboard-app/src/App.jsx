import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bell, 
  Search, 
  Star, 
  TrendingDown, 
  TrendingUp, 
  ShieldCheck, 
  Activity, 
  Users, 
  Lock,
  Download,
  AlertTriangle,
  Package,
  Gavel,
  LineChart,
  LayoutDashboard,
  Coins,
  ArrowUpRight,
  ArrowDownRight,
  Newspaper,
  FileText,
  Layout,
  Trash2,
  Award,
  Bot,
  BookOpen,
  RotateCcw
} from 'lucide-react';

// --- Emergency Guide Modal ---
const EmergencyGuideModal = ({ isOpen, onClose }) => (
  <AnimatePresence>
    {isOpen && (
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        />
        <motion.div 
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="relative w-full max-w-2xl bg-surface-container-high border border-outline-variant rounded-3xl shadow-2xl overflow-hidden"
        >
          <div className="bg-primary/10 px-8 py-6 border-b border-outline-variant">
            <h2 className="text-2xl font-bold text-primary flex items-center gap-3">
              <ShieldCheck size={28} /> 긴급 대응 지침 (Standard Operating Procedure)
            </h2>
            <p className="text-on-surface-variant text-sm mt-1">시장 변동성 급증 시 구매팀 액션 가이드</p>
          </div>
          <div className="p-8 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar text-on-surface">
            <div className="space-y-4">
              <h3 className="font-bold text-error flex items-center gap-2 text-lg">LEVEL 1: 환율/원자재 5% 이상 변동 시</h3>
              <ul className="space-y-3 text-sm">
                <li className="flex gap-3 items-start">
                  <span className="w-6 h-6 rounded-full bg-error/10 text-error flex items-center justify-center text-xs font-bold shrink-0">1</span>
                  <span>전략 물자(철강, 구리) 수입 결제 시점 즉시 재검토 및 선물환 계약 비중 확대</span>
                </li>
                <li className="flex gap-3 items-start">
                  <span className="w-6 h-6 rounded-full bg-error/10 text-error flex items-center justify-center text-xs font-bold shrink-0">2</span>
                  <span>에스컬레이션(V/O) 조항 발동 여부 검토 및 협력사 단가 보전 협의 착수</span>
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="font-bold text-secondary flex items-center gap-2 text-lg">LEVEL 2: 공급망 중단 및 물류 마비 시</h3>
              <ul className="space-y-3 text-sm">
                <li className="flex gap-3 items-start">
                  <span className="w-6 h-6 rounded-full bg-secondary/10 text-secondary flex items-center justify-center text-xs font-bold shrink-0">1</span>
                  <span>대체 공급선(Alt-Source) 가동 및 긴급 안전 재고 확보 (최소 3개월분)</span>
                </li>
                <li className="flex gap-3 items-start">
                  <span className="w-6 h-6 rounded-full bg-secondary/10 text-secondary flex items-center justify-center text-xs font-bold shrink-0">2</span>
                  <span>항공 운송 등 비상 물류 루트 확보 및 물류비 증액분 긴급 품의 진행</span>
                </li>
              </ul>
            </div>
          </div>
          <div className="p-6 bg-surface-container-low flex justify-end gap-3 border-t border-outline-variant">
            <button 
              onClick={onClose}
              className="px-6 py-2.5 rounded-xl text-xs font-bold text-on-surface-variant hover:bg-white/5 transition-all"
            >
              닫기
            </button>
            <button className="bg-primary text-on-primary px-8 py-2.5 rounded-xl text-xs font-bold hover:brightness-110 shadow-lg shadow-primary/20">
              지침서 다운로드 (PDF)
            </button>
          </div>
        </motion.div>
      </div>
    )}
  </AnimatePresence>
);

// --- View 1: 시장 지표 대시보드 ---
const DashboardView = ({ currency, setCurrency, updateTime }) => {
  const [isGuideOpen, setIsGuideOpen] = useState(false);
  const currencyData = {
    USD: { 
      label: 'USD / KRW (원/달러)', 
      value: '1,458.50', 
      change: '+1.2%', 
      trend: 'up',
      // 12주(3개월) 주단위 데이터
      history: [1380, 1405, 1395, 1410, 1425, 1420, 1435, 1445, 1440, 1450, 1445, 1458]
    },
    JPY: { 
      label: 'JPY / KRW (100엔/원)', 
      value: '925.10', 
      change: '+0.45%', 
      trend: 'up',
      history: [880, 890, 905, 900, 910, 905, 915, 920, 918, 922, 920, 925]
    },
    EUR: { 
      label: 'EUR / KRW (원/유로)', 
      value: '1,703.26', 
      change: '-0.15%', 
      trend: 'down',
      history: [1740, 1735, 1745, 1730, 1720, 1725, 1715, 1710, 1705, 1708, 1712, 1703]
    }
  };

  const selectedData = currencyData[currency];

  // Curve Generation Logic for SVG
  const generatePath = (data) => {
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min;
    const width = 200;
    const height = 50;
    
    const points = data.map((val, i) => ({
      x: (i / (data.length - 1)) * width,
      y: height - ((val - min) / range) * height
    }));

    return points.reduce((path, point, i) => {
      if (i === 0) return `M ${point.x},${point.y}`;
      const prev = points[i - 1];
      const cx = (prev.x + point.x) / 2;
      return `${path} C ${cx},${prev.y} ${cx},${point.y} ${point.x},${point.y}`;
    }, "");
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} 
      animate={{ opacity: 1, y: 0 }} 
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      <EmergencyGuideModal isOpen={isGuideOpen} onClose={() => setIsGuideOpen(false)} />
      
      <section className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-primary mb-1">시장 지표 (Real-time)</h2>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-secondary animate-pulse"></div>
            <p className="text-on-surface-variant text-sm font-medium">최종 업데이트: {updateTime} (1시간 단위 자동 갱신)</p>
          </div>
        </div>
        <div className="flex bg-surface-container-high rounded-xl p-1 gap-1 border border-outline-variant">
          {['USD', 'JPY', 'EUR'].map((c) => (
            <button 
              key={c} 
              onClick={() => setCurrency(c)}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${currency === c ? 'bg-primary text-background shadow-lg' : 'text-on-surface-variant hover:text-on-surface'}`}
            >
              {c}
            </button>
          ))}
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Main Exchange Rate Card with 12W Curve Trend */}
        <div className="glass-card col-span-1 md:col-span-3 border-l-4 border-primary p-6">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
                <Coins size={24} />
              </div>
              <div>
                <p className="text-xs uppercase tracking-wider text-on-surface-variant mb-1">{selectedData.label}</p>
                <div className="flex items-baseline gap-2">
                  <p className="text-4xl font-bold font-space text-on-surface">{selectedData.value}</p>
                  <span className={`flex items-center text-sm font-bold ${selectedData.trend === 'up' ? 'text-error' : 'text-tertiary'}`}>
                    {selectedData.trend === 'up' ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
                    {selectedData.change}
                  </span>
                </div>
              </div>
            </div>
            <div className="flex-1 max-w-[300px] ml-8">
              <div className="flex justify-between items-center mb-2">
                <p className="text-[10px] font-bold text-on-surface-variant uppercase">3-Month Trend (Weekly)</p>
                <span className="text-[9px] text-primary font-bold">12 Weeks History</span>
              </div>
              <svg viewBox="0 0 200 60" className="w-full h-12 overflow-visible">
                <defs>
                  <linearGradient id="curveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.2" />
                    <stop offset="100%" stopColor="#38bdf8" stopOpacity="1" />
                  </linearGradient>
                  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>
                <motion.path
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 1.5, ease: "easeInOut" }}
                  d={generatePath(selectedData.history)}
                  fill="none"
                  stroke="url(#curveGradient)"
                  strokeWidth="3"
                  strokeLinecap="round"
                  filter="url(#glow)"
                />
                {/* Last point circle */}
                <circle 
                  cx="200" 
                  cy={50 - ((selectedData.history[11] - Math.min(...selectedData.history)) / (Math.max(...selectedData.history) - Math.min(...selectedData.history))) * 50} 
                  r="4" 
                  fill="#38bdf8" 
                  className="animate-pulse"
                />
              </svg>
            </div>
          </div>
          <div className="h-[1px] w-full bg-outline-variant mb-4 opacity-50"></div>
          <p className="text-[11px] text-on-surface-variant italic">※ 12주 주단위 추세 분석 결과: {selectedData.trend === 'up' ? '상승 압력 지속' : '박스권 하향 돌파'} 국면 (전략적 결제 시점 검토 요망)</p>
        </div>

        {/* Triple Indicators */}
        <div className="glass-card border-t-2 border-secondary/30">
          <p className="text-xs uppercase tracking-wider text-on-surface-variant mb-1">Gold (spot oz)</p>
          <p className="text-2xl font-bold font-space text-on-surface">$4,705.20</p>
          <div className="mt-4 flex justify-between items-end">
            <span className="text-error text-xs font-bold">+2.15% 급등</span>
            <div className="h-6 w-16 bg-error/10 rounded overflow-hidden">
               <div className="h-full w-full bg-error/40" style={{ clipPath: 'polygon(0 80%, 25% 60%, 50% 40%, 75% 20%, 100% 10%, 100% 100%, 0 100%)' }}></div>
            </div>
          </div>
        </div>

        <div className="glass-card border-t-2 border-primary/30">
          <p className="text-xs uppercase tracking-wider text-on-surface-variant mb-1">Copper (LME/MT)</p>
          <p className="text-2xl font-bold font-space text-on-surface">$13,391.50</p>
          <div className="mt-4 flex justify-between items-end">
            <span className="text-on-tertiary-container text-xs font-bold">+0.84%</span>
            <div className="h-6 w-16 bg-tertiary-container rounded overflow-hidden">
               <div className="h-full w-full bg-on-tertiary-container/40" style={{ clipPath: 'polygon(0 80%, 25% 60%, 50% 40%, 75% 20%, 100% 10%, 100% 100%, 0 100%)' }}></div>
            </div>
          </div>
        </div>

        <div className="glass-card border-t-2 border-tertiary/30">
          <p className="text-xs uppercase tracking-wider text-on-surface-variant mb-1">Brent Oil (bbl)</p>
          <p className="text-2xl font-bold font-space text-on-surface">$101.27</p>
          <div className="mt-4 flex justify-between items-end">
            <span className="text-tertiary text-xs font-bold">-1.8% 하락</span>
            <div className="h-6 w-16 bg-tertiary/10 rounded overflow-hidden">
               <div className="h-full w-full bg-tertiary/40" style={{ clipPath: 'polygon(0 20%, 25% 40%, 50% 60%, 75% 80%, 100% 90%, 100% 100%, 0 100%)' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Active Alerts */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-3">
            <h3 className="text-xs uppercase tracking-widest text-on-surface-variant font-bold">Active Alerts (4)</h3>
            <span className="text-[9px] bg-secondary/10 text-secondary border border-secondary/20 px-2 py-0.5 rounded-full font-bold animate-pulse">{updateTime.split(' ')[1]} 동시 업데이트</span>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={() => setIsGuideOpen(true)}
              className="bg-error/10 hover:bg-error/20 text-error text-[10px] font-bold px-3 py-1 rounded-full border border-error/20 flex items-center gap-1 transition-all"
            >
              <ShieldCheck size={12} /> 긴급 대응 지침 확인
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="flex items-center gap-4 p-4 bg-error-container/10 border-l-4 border-error rounded-xl glass-panel">
            <TrendingUp className="text-error w-5 h-5" />
            <div className="flex-1">
              <p className="text-sm font-bold">{currency} 환율 변동성 임계치 도달</p>
              <p className="text-[10px] text-on-surface-variant">수입 결제 시점 조정 권고</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-secondary-container/10 border-l-4 border-secondary rounded-xl glass-panel">
            <AlertTriangle className="text-secondary w-5 h-5" />
            <div className="flex-1">
              <p className="text-sm font-bold">중동 지정학적 리스크 심화</p>
              <p className="text-[10px] text-on-surface-variant">해상 물류비(SCFI) 급등 우려</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-primary-container/10 border-l-4 border-primary rounded-xl glass-panel">
            <Activity className="text-primary w-5 h-5" />
            <div className="flex-1">
              <p className="text-sm font-bold">국내 산업용 전기요금 추가 인상 가능성</p>
              <p className="text-[10px] text-on-surface-variant">에너지 다소비 자재(시멘트 등) 단가 영향</p>
            </div>
          </div>
          <div className="flex items-center gap-4 p-4 bg-tertiary-container/10 border-l-4 border-tertiary rounded-xl glass-panel">
            <ArrowUpRight className="text-tertiary w-5 h-5" />
            <div className="flex-1">
              <p className="text-sm font-bold">중국 철강 생산 감축 본격화</p>
              <p className="text-[10px] text-on-surface-variant">국내 열연/철근 유통가 반등 전조</p>
            </div>
          </div>
        </div>
      </section>

      {/* Market Intelligence (Construction/Plant) */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <Newspaper size={18} className="text-primary" />
          <h3 className="text-lg font-bold text-on-surface">건설·식품플랜트사업 원부자재 Intelligence (국내 중심)</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="glass-panel p-5 rounded-2xl border border-outline-variant hover:border-primary/40 hover:bg-primary/5 transition-all group">
            <div className="flex justify-between items-start mb-3">
              <span className="text-[10px] font-bold bg-error/10 text-error px-2.5 py-1 rounded-lg">철강 (Steel)</span>
              <span className="text-[9px] text-primary font-bold">{updateTime.split(' ')[1]} 업데이트</span>
            </div>
            <h4 className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">국내 주요 제철사, 3월 출하가 5% 인상 결정</h4>
            <p className="text-[11px] text-on-surface-variant mt-2 leading-relaxed">
              포스코, 현대제철 등 국내 주요 제철사가 산업용 전기료 인상분과 원료탄 가격 상승을 반영하여 H형강 및 철근 가격 인상을 단행했습니다. 건설 현장 원가 압박 가중 예상.
            </p>
          </div>
          <div className="glass-panel p-5 rounded-2xl border border-outline-variant hover:border-secondary/40 hover:bg-secondary/5 transition-all group">
            <div className="flex justify-between items-start mb-3">
              <span className="text-[10px] font-bold bg-secondary/10 text-secondary px-2.5 py-1 rounded-lg">전기 (Cable)</span>
              <span className="text-[9px] text-primary font-bold">{updateTime.split(' ')[1]} 업데이트</span>
            </div>
            <h4 className="text-sm font-bold text-on-surface group-hover:text-secondary transition-colors">LS전선·대한전선, 구리 시세 연동 단가 에스컬레이션</h4>
            <p className="text-[11px] text-on-surface-variant mt-2 leading-relaxed">
              LME 구리 가격이 톤당 1.3만 달러를 돌파하며 전력 케이블 납품가가 급등하고 있습니다. 공공 플랜트 사업의 경우 물가 변동에 따른 계약 금액 조정 신청이 급증하고 있습니다.
            </p>
          </div>
          <div className="glass-panel p-5 rounded-2xl border border-outline-variant hover:border-tertiary/40 hover:bg-tertiary/5 transition-all group">
            <div className="flex justify-between items-start mb-3">
              <span className="text-[10px] font-bold bg-tertiary/10 text-tertiary px-2.5 py-1 rounded-lg">식품플랜트사업 자재</span>
              <span className="text-[9px] text-primary font-bold">{updateTime.split(' ')[1]} 업데이트</span>
            </div>
            <h4 className="text-sm font-bold text-on-surface group-hover:text-tertiary transition-colors">식품플랜트사업 위생 배관재 납기 지연 우려</h4>
            <p className="text-[11px] text-on-surface-variant mt-2 leading-relaxed">
              니켈 등 비철금속 가격 불안정으로 스테인리스 강관 수급이 원활하지 않습니다. 특히 식품 전용 위생 배관재의 경우 국내 재고 부족으로 프로젝트 납기가 평균 2주 지연 중입니다.
            </p>
          </div>
        </div>
      </section>
    </motion.div>
  );
};

// --- 신규: 데이터 입력/수정 모달 ---
const InputModal = ({ isOpen, onClose, data, onSave }) => {
  const [formData, setFormData] = useState(data);
  const [isParsing, setIsParsing] = useState(false);
  const [isQuotationParsing, setIsQuotationParsing] = useState(false);
  const [useBM, setUseBM] = useState(true);
  const [useQuotationBM, setUseQuotationBM] = useState(false);

  useEffect(() => {
    if (data) {
      setFormData({
        ...data,
        quotationBreakdown: data.quotationBreakdown || { material: 0, labor: 0, expense: 0 }
      });
    }
  }, [data]);

  const handleChange = (field, value) => {
    const numValue = parseInt(value.replace(/,/g, '')) || 0;
    setFormData(prev => {
      const next = { ...prev };
      if (field.includes('.')) {
        const [parent, child] = field.split('.');
        next[parent] = { ...next[parent], [child]: numValue };
        
        // 실시간 총액 재계산
        if (parent === 'breakdown') {
          next.baseCost = (next.breakdown.material || 0) + (next.breakdown.labor || 0) + (next.breakdown.expense || 0);
        } else if (parent === 'quotationBreakdown') {
          next.quotationCost = (next.quotationBreakdown.material || 0) + (next.quotationBreakdown.labor || 0) + (next.quotationBreakdown.expense || 0);
        }
      } else {
        next[field] = value;
      }
      return next;
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[110] flex items-center justify-center p-4">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} onClick={onClose} className="absolute inset-0 bg-black/80 backdrop-blur-md" />
      <motion.div 
        initial={{ scale: 0.9, opacity: 0 }} 
        animate={{ scale: 1, opacity: 1 }} 
        className="relative w-full max-w-3xl bg-slate-900 border border-white/10 rounded-3xl p-8 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar"
      >
        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2 notranslate" translate="no">
          <Activity size={20} className="text-primary"/> 품셈 및 견적 분석 설정
        </h3>

        {/* 프로젝트명 수정 필드 추가 */}
        <div className="mb-8 p-4 bg-white/5 rounded-2xl border border-white/10">
          <label className="text-[10px] text-primary font-bold block mb-2 uppercase tracking-widest notranslate" translate="no">분석 프로젝트명 수정</label>
          <input 
            type="text" 
            value={formData.title} 
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="프로젝트명을 입력하세요"
            className="w-full bg-slate-800 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:border-primary/50 outline-none transition-all font-bold"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* LEFT: 기준 예가 (BM) */}
          <section className="space-y-6">
            <div className="flex justify-between items-center">
              <h4 className="text-xs font-bold text-primary uppercase tracking-widest flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                1. 기준 예가 (BM/정부품셈)
              </h4>
              <div className="flex bg-white/5 rounded-lg p-0.5 border border-white/10">
                <button onClick={() => setUseBM(true)} className={`px-2 py-1 text-[9px] rounded-md transition-all ${useBM ? 'bg-primary text-slate-900 font-bold' : 'text-slate-400'}`}>BM 연동</button>
                <button onClick={() => setUseBM(false)} className={`px-2 py-1 text-[9px] rounded-md transition-all ${!useBM ? 'bg-primary text-slate-900 font-bold' : 'text-slate-400'}`}>수동</button>
              </div>
            </div>

            {useBM ? (
              <div className="relative group">
                <input type="file" accept=".pdf" className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                  onChange={(e) => {
                    setIsParsing(true);
                    setTimeout(() => {
                      setFormData(prev => ({
                        ...prev,
                        breakdown: { material: 220000000, labor: 150000000, expense: 80000000 },
                        baseCost: 450000000
                      }));
                      setIsParsing(false);
                    }, 1000);
                  }}
                />
                <div className="bg-primary/5 border border-dashed border-primary/30 rounded-2xl p-6 text-center group-hover:bg-primary/10 transition-all">
                  {isParsing ? <div className="animate-spin w-4 h-4 border-2 border-primary border-t-transparent rounded-full mx-auto" /> : <FileText size={20} className="text-primary mx-auto mb-2"/>}
                  <p className="text-[10px] text-white font-bold notranslate" translate="no">기준 BM PDF 업로드</p>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">자재비 (₩)</label>
                  <input type="text" value={(formData.breakdown?.material || 0).toLocaleString()} onChange={(e) => handleChange('breakdown.material', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">인건비 (₩)</label>
                  <input type="text" value={(formData.breakdown?.labor || 0).toLocaleString()} onChange={(e) => handleChange('breakdown.labor', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1 notranslate" translate="no">간접비/제경비 (₩)</label>
                  <input type="text" value={(formData.breakdown?.expense || 0).toLocaleString()} onChange={(e) => handleChange('breakdown.expense', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
              </div>
            )}
            {/* 총액 표시 박스 (기준) */}
            <div className="pt-4 border-t border-white/10">
              <label className="text-[9px] text-primary font-bold block mb-1 uppercase tracking-widest">기준 총 합계 (₩)</label>
              <div className="w-full bg-primary/10 border border-primary/30 rounded-2xl px-4 py-4 text-xl text-primary font-bold font-space flex justify-between items-center">
                <span className="text-xs text-primary/60 font-bold notranslate" translate="no">TOTAL</span>
                <span className="notranslate" translate="no">₩{(formData.baseCost || 0).toLocaleString()}</span>
              </div>
            </div>
          </section>

          {/* RIGHT: 견적사 견적가 */}
          <section className="space-y-6">
            <div className="flex justify-between items-center">
              <h4 className="text-xs font-bold text-secondary uppercase tracking-widest flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse" />
                2. 소싱업체 제출가 (최종 제출)
              </h4>
              <div className="flex bg-white/5 rounded-lg p-0.5 border border-white/10">
                <button onClick={() => setUseQuotationBM(true)} className={`px-2 py-1 text-[9px] rounded-md transition-all ${useQuotationBM ? 'bg-secondary text-slate-900 font-bold' : 'text-slate-400'}`}>견적서 연동</button>
                <button onClick={() => setUseQuotationBM(false)} className={`px-2 py-1 text-[9px] rounded-md transition-all ${!useQuotationBM ? 'bg-secondary text-slate-900 font-bold' : 'text-slate-400'}`}>수동</button>
              </div>
            </div>

            {useQuotationBM ? (
              <div className="relative group">
                <input type="file" accept=".pdf" className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                  onChange={(e) => {
                    setIsQuotationParsing(true);
                    setTimeout(() => {
                      setFormData(prev => ({
                        ...prev,
                        quotationBreakdown: { material: 235000000, labor: 145000000, expense: 85000000 },
                        quotationCost: 465000000
                      }));
                      setIsQuotationParsing(false);
                    }, 1000);
                  }}
                />
                <div className="bg-secondary/5 border border-dashed border-secondary/30 rounded-2xl p-6 text-center group-hover:bg-secondary/10 transition-all">
                  {isQuotationParsing ? <div className="animate-spin w-4 h-4 border-2 border-secondary border-t-transparent rounded-full mx-auto" /> : <FileText size={20} className="text-secondary mx-auto mb-2"/>}
                  <p className="text-[10px] text-white font-bold">소싱업체 제출서류 PDF 업로드</p>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">견적 자재비 (₩)</label>
                  <input type="text" value={(formData.quotationBreakdown?.material || 0).toLocaleString()} onChange={(e) => handleChange('quotationBreakdown.material', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">견적 인건비 (₩)</label>
                  <input type="text" value={(formData.quotationBreakdown?.labor || 0).toLocaleString()} onChange={(e) => handleChange('quotationBreakdown.labor', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
                <div>
                  <label className="text-[9px] text-slate-500 block mb-1">견적 간접비/제경비 (₩)</label>
                  <input type="text" value={(formData.quotationBreakdown?.expense || 0).toLocaleString()} onChange={(e) => handleChange('quotationBreakdown.expense', e.target.value)} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white font-mono" />
                </div>
              </div>
            )}
            {/* 총액 표시 박스 (견적) */}
            <div className="pt-4 border-t border-white/10">
              <label className="text-[9px] text-secondary font-bold block mb-1 uppercase tracking-widest">견적 총 합계 (₩)</label>
              <div className="w-full bg-secondary/10 border border-secondary/30 rounded-2xl px-4 py-4 text-xl text-secondary font-bold font-space flex justify-between items-center">
                <span className="text-xs text-secondary/60 font-bold">TOTAL</span>
                <span>₩{(formData.quotationCost || 0).toLocaleString()}</span>
              </div>
            </div>
          </section>
        </div>

        {/* 견적사 목록 관리 (추가 요청 사항) */}
        <section className="mt-8 pt-8 border-t border-white/10">
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center gap-2">
              <Users size={18} className="text-secondary" />
              <h4 className="text-xs font-bold text-white uppercase tracking-widest">소싱업체별 제출가 관리 (최대 5개)</h4>
            </div>
            {formData.vendors.length < 5 && (
              <button 
                onClick={() => {
                  setFormData(prev => ({
                    ...prev,
                    vendors: [...prev.vendors, { name: '', quote: 0 }]
                  }));
                }}
                className="text-[10px] bg-secondary/20 text-secondary border border-secondary/30 px-3 py-1.5 rounded-xl hover:bg-secondary/30 transition-all font-bold"
              >
                + 소싱업체 추가
              </button>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {formData.vendors.map((vendor, idx) => (
              <div key={idx} className="flex gap-3 items-end bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-white/10 transition-all group">
                <div className="flex-1">
                  <label className="text-[8px] text-slate-500 mb-1 block font-bold uppercase">소싱업체 {idx + 1} 명칭</label>
                  <input 
                    type="text" 
                    value={vendor.name} 
                    onChange={(e) => {
                      const newVendors = [...formData.vendors];
                      newVendors[idx].name = e.target.value;
                      setFormData({...formData, vendors: newVendors});
                    }}
                    placeholder="업체명 입력"
                    className="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:border-secondary/50 outline-none transition-all"
                  />
                </div>
                <div className="flex-[1.2]">
                  <label className="text-[8px] text-slate-500 mb-1 block font-bold uppercase">제출 총액 (₩)</label>
                  <input 
                    type="text" 
                    value={vendor.quote.toLocaleString()} 
                    onChange={(e) => {
                      const val = parseInt(e.target.value.replace(/,/g, '')) || 0;
                      const newVendors = [...formData.vendors];
                      newVendors[idx].quote = val;
                      setFormData({...formData, vendors: newVendors});
                    }}
                    className="w-full bg-slate-800 border border-white/10 rounded-xl px-3 py-2 text-xs text-white font-mono focus:border-secondary/50 outline-none transition-all"
                  />
                </div>
                <button 
                  onClick={() => {
                    const newVendors = formData.vendors.filter((_, i) => i !== idx);
                    setFormData({...formData, vendors: newVendors});
                  }}
                  className="p-2 text-slate-600 hover:text-error transition-colors bg-white/5 rounded-lg opacity-0 group-hover:opacity-100"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
            {formData.vendors.length === 0 && (
              <div className="col-span-2 py-8 text-center border-2 border-dashed border-white/5 rounded-3xl">
                <p className="text-[10px] text-slate-500 font-bold uppercase">등록된 소싱업체가 없습니다. 우측 상단 버튼을 눌러 추가하세요.</p>
              </div>
            )}
          </div>
        </section>

        <div className="flex justify-end gap-3 mt-8">
          <button onClick={onClose} className="px-6 py-2 rounded-xl text-xs font-bold text-slate-400 hover:bg-white/5">취소</button>
          <button 
            onClick={() => { onSave(formData); onClose(); }}
            className="bg-primary text-slate-900 px-8 py-2 rounded-xl text-xs font-bold hover:brightness-110 shadow-lg shadow-primary/20 notranslate"
            translate="no"
          >
            데이터 분석 적용
          </button>
        </div>
      </motion.div>
    </div>
  );
};

// --- View 2: 품셈분석 (CostStandardView) ---
const CostStandardView = () => {
  const [selectedCategory, setSelectedCategory] = useState('intelligence');
  const [isInputOpen, setIsInputOpen] = useState(false);
  
  // 상태로 관리하여 사용자가 입력 가능하도록 변경
  const [standardData, setStandardData] = useState({
    food: {
      title: "식품플랜트사업",
      baseCost: 450000000,
      breakdown: { material: 220000000, labor: 150000000, expense: 80000000 },
      quotationCost: 465000000,
      quotationBreakdown: { material: 235000000, labor: 145000000, expense: 85000000 },
      vendors: []
    },
    construction: {
      title: "건설사업",
      baseCost: 1200000000,
      breakdown: { material: 650000000, labor: 400000000, expense: 150000000 },
      quotationCost: 1180000000,
      quotationBreakdown: { material: 630000000, labor: 410000000, expense: 140000000 },
      vendors: []
    },
    intelligence: {
      title: "지능화사업",
      baseCost: 850000000,
      breakdown: { material: 400000000, labor: 350000000, expense: 100000000 },
      quotationCost: 820000000,
      quotationBreakdown: { material: 380000000, labor: 340000000, expense: 100000000 },
      vendors: []
    }
  });

  const handleSave = (newData) => {
    // 깊은 복사를 통해 참조를 끊고 순수 데이터만 저장 (정지 현상 방지)
    const sanitizedData = JSON.parse(JSON.stringify(newData));
    setStandardData(prev => ({
      ...prev,
      [selectedCategory]: sanitizedData
    }));
  };

  const current = standardData[selectedCategory] || { title: "N/A", baseCost: 0, breakdown: {}, quotationBreakdown: {}, vendors: [] };
  
  // 최저가 견적사 도출
  const lowestVendor = current.vendors && current.vendors.length > 0 
    ? current.vendors.reduce((prev, curr) => (prev.quote < curr.quote ? prev : curr))
    : null;
    
  const displayQuotationCost = lowestVendor ? lowestVendor.quote : current.quotationCost;

  const deviation = (val, base) => {
    if (!base || isNaN(base) || base === 0) return "0.0";
    const v = isNaN(val) ? 0 : val;
    return ((v - base) / base * 100).toFixed(1);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, x: 20 }} 
      animate={{ opacity: 1, x: 0 }} 
      exit={{ opacity: 0, x: -20 }}
      className="space-y-6"
    >
      <InputModal 
        isOpen={isInputOpen} 
        onClose={() => setIsInputOpen(false)} 
        data={current} 
        onSave={handleSave} 
      />

      <header className="flex justify-between items-end">
        <div className="notranslate" translate="no">
          <p className="text-xs text-on-surface-variant uppercase tracking-widest mb-1">비용 분석 시스템</p>
          <h2 className="text-3xl font-bold text-primary font-space">품셈분석 예측</h2>
          <div className="flex items-center gap-2 mt-2">
            <div className="w-2 h-2 rounded-full bg-secondary animate-pulse"></div>
            <p className="text-[11px] text-on-surface-variant">정부 공인 엔지니어링 대가산정 서비스 실시간 연동 중 (객관적 지표)</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex bg-surface-container-high rounded-2xl p-1 border border-outline-variant">
            {Object.keys(standardData).map(key => (
              <button
                key={key}
                onClick={() => setSelectedCategory(key)}
                className={`px-4 py-1.5 rounded-xl text-[11px] font-bold transition-all notranslate ${
                  selectedCategory === key ? 'bg-primary text-background' : 'text-on-surface-variant hover:text-on-surface'
                }`}
                translate="no"
              >
                {standardData[key].title}
              </button>
            ))}
          </div>
          <button 
            onClick={() => setIsInputOpen(true)}
            className="bg-white/5 border border-white/10 hover:bg-white/10 px-4 py-2 rounded-2xl text-[11px] font-bold text-white flex items-center gap-2 transition-all active:scale-95 notranslate"
            translate="no"
          >
            <Package size={14} className="text-primary" /> 데이터 입력/수정
          </button>
        </div>
      </header>
      {/* 프로젝트 요약 정보 */}
      <div className="flex flex-col md:flex-row justify-between items-center glass-card p-6 border-l-4 border-l-primary">
        <div className="flex items-center gap-4 mb-4 md:mb-0">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center">
            <Layout size={24} className="text-primary" />
          </div>
          <div className="notranslate" translate="no">
            <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">품셈분석 프로젝트명</p>
            <h3 className="text-xl font-bold text-on-surface">{current.title}</h3>
          </div>
        </div>
        <div className="flex items-center gap-8 notranslate" translate="no">
          <div className="text-right">
            <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">기준 예가</p>
            <p className="text-2xl font-bold text-primary font-space">₩{current.baseCost.toLocaleString()}</p>
          </div>
          <div className="h-10 w-px bg-outline-variant hidden md:block" />
          <div className="text-right">
            <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">
              {lowestVendor ? `소싱 최저가 (${lowestVendor.name})` : "소싱업체 제출가"}
            </p>
            <p className="text-2xl font-bold text-secondary font-space">₩{displayQuotationCost.toLocaleString()}</p>
          </div>
          <div className="h-10 w-px bg-outline-variant hidden md:block" />
          <div className="text-right">
            <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-1">편차율</p>
            <p className={`text-2xl font-bold font-space ${parseFloat(deviation(displayQuotationCost, current.baseCost)) > 0 ? 'text-error' : 'text-secondary'}`}>
              {deviation(displayQuotationCost, current.baseCost)}%
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* 항목별 1:1 비교 섹션 */}
        {[
          { label: '자재비', key: 'material' },
          { label: '인건비', key: 'labor' },
          { label: '간접비/제경비', key: 'expense' }
        ].map(item => (
          <div key={item.key} className="glass-card border-t-2 border-primary/20 p-6 notranslate" translate="no">
            <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-4">{item.label} 비교</p>
            <div className="space-y-4">
              <div className="flex justify-between items-end">
                <span className="text-[11px] text-slate-500">기준 예가</span>
                <span className="text-lg font-bold text-on-surface">₩{(current.breakdown?.[item.key] || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-end pb-2 border-b border-white/5">
                <span className="text-[11px] text-slate-500">소싱업체 제출가</span>
                <span className="text-lg font-bold text-secondary">₩{(current.quotationBreakdown?.[item.key] || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-[10px] font-bold text-on-surface-variant">편차율</span>
                <span className={`text-sm font-bold ${parseFloat(deviation(current.quotationBreakdown?.[item.key], current.breakdown?.[item.key])) > 0 ? 'text-error' : 'text-secondary'}`}>
                  {deviation(current.quotationBreakdown?.[item.key], current.breakdown?.[item.key])}%
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

        {/* 견적사 자동 비교 분석 */}
        <div className="lg:col-span-2 glass-card p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-sm font-bold flex items-center gap-2">
              <TrendingUp size={18} className="text-secondary"/>
              소싱업체별 제출가 자동 비교 분석
            </h3>
            <span className="text-[10px] text-on-surface-variant">데이터 소스: 정부 공인 표준품셈 DB</span>
          </div>
          
          <div className="space-y-3 max-h-[300px] overflow-y-auto custom-scrollbar pr-2">
            {current.vendors.map((v, i) => {
              const diff = parseFloat(deviation(v.quote, current.baseCost));
              const isHigh = diff > 0;
              return (
                <div key={i} className="flex items-center justify-between p-4 bg-surface-container-low rounded-2xl border border-outline-variant hover:border-primary/30 transition-all">
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold ${isHigh ? 'bg-error/10 text-error' : 'bg-secondary/10 text-secondary'}`}>
                      {v.name ? v.name[0] : '?'}
                    </div>
                    <div className="notranslate" translate="no">
                      <div className="text-sm font-bold text-on-surface">{v.name || '미지정 업체'}</div>
                      <div className="text-[10px] text-on-surface-variant">제출가: ₩{v.quote.toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="text-right notranslate" translate="no">
                    <div className={`text-sm font-bold flex items-center justify-end gap-1 ${isHigh ? 'text-error' : 'text-secondary'}`}>
                      {isHigh ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                      {Math.abs(diff)}%
                    </div>
                    <div className="text-[9px] text-on-surface-variant font-bold">
                      공인 품셈 대비 {isHigh ? '초과' : '절감'}
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      </div>
    </motion.div>
  );
};

// --- View 3: 업체소싱 추천 (SourcingView) ---
const SourcingView = () => {
  const [isSourcing, setIsSourcing] = useState(false);
  const [inputs, setInputs] = useState({ category: '', region: '', license: '' });

  const sourcingCriteria = {
    revenue: "10억 ~ 1000억",
    credit: "B 이상 (B+ 권장)",
    record: "최근 2개년 (2024, 2025) 실적 보유",
    region: "전국구 및 프로젝트 거점"
  };

  const defaultVendors = [
    { id: 1, name: '농심엔지니어링(주)', specialty: '식품/제약 플랜트, 스마트팩토리', revenue: '852억', credit: 'A-', records: ['2024: 식품 가공라인 자동화 12건'], region: '전국구 (경기 거점)', licenses: ['종합건설업', '기계설비', '전기공사'], phone: '02-827-2681' },
    { id: 2, name: '(주)시스템알앤디', specialty: '푸드테크, 자동화 생산라인', revenue: '425억', credit: 'BBB+', records: ['2024: 음료 살균 시스템 구축 15건'], region: '경상/전라 거점', licenses: ['소프트웨어', '정보통신', '제조업'], phone: '031-456-7890' },
    { id: 3, name: '(주)유테크엔지니어링', specialty: '바이오/식품 플랜트 엔지니어링', revenue: '289억', credit: 'BBB', records: ['2024: 해썹(HACCP) 인증 설비 20건'], region: '수도권 거점', licenses: ['가스시설', '강구조물', '냉난방'], phone: '02-345-6789' },
    { id: 4, name: '(주)영진에프엠씨', specialty: '추출/농축 및 식품 제조 장비', revenue: '156억', credit: 'B+', records: ['2024: 농축 설비 유지보수 30건'], region: '충청/강원 특화', licenses: ['상하수도', '금속창호', '특수장비'], phone: '042-789-0123' },
    { id: 5, name: '(주)대동에프앤비', specialty: '지능화 공정 제어 시스템', revenue: '124억', credit: 'B+', records: ['2024: 스마트 공정 센서 8건'], region: '경기 거점', licenses: ['계측기기', '자동제어', '엔지니어링'], phone: '031-234-5678' },
    { id: 6, name: '(주)한성시스템', specialty: '공정 자동화 하드웨어', revenue: '95억', credit: 'B0', records: ['2024: 컨베이어 제어 시스템 12건'], region: '전라 거점', licenses: ['전기공사', '정밀기계'], phone: '062-345-6789' },
    { id: 7, name: '(주)미래푸드테크놀로지', specialty: '식품 가공 로봇 솔루션', revenue: '82억', credit: 'B+', records: ['2024: 로봇 팔 패키징 도입 5건'], region: '충청 거점', licenses: ['소프트웨어', '로봇제조'], phone: '041-567-8901' },
    { id: 8, name: '(주)세종플랜트산업', specialty: '대형 식품 저장 탱크 제작', revenue: '71억', credit: 'B-', records: ['2024: 대용량 사일로 설치 8건'], region: '경상 거점', licenses: ['특수창호', '강구조물'], phone: '051-678-9012' },
    { id: 9, name: '(주)글로벌엔지니어링', specialty: '해외 플랜트 설계 지원', revenue: '65억', credit: 'B0', records: ['2024: 베트남 가공 공장 설계'], region: '전국구', licenses: ['엔지니어링', '설계전문'], phone: '02-901-2345' },
    { id: 10, name: '(주)에이치에스기술', specialty: '스마트 팩토리 유지보수', revenue: '58억', credit: 'B+', records: ['2024: 공정 최적화 컨설팅 20건'], region: '경기 거점', licenses: ['정보통신', '전기공사'], phone: '031-890-1234' }
  ];

  const [displayVendors, setDisplayVendors] = useState(defaultVendors);

  const handleSourcing = () => {
    setIsSourcing(true);
    
    setTimeout(() => {
      const category = inputs.category || '전문공사';
      const region = inputs.region || '전국';
      const userLicense = inputs.license || '전문면허';
      
      const newVendors = Array.from({ length: 10 }, (_, i) => {
        const prefix = ['대한', '우리', '현대', '신세계', '미래', '한성', '세종', '글로벌', '에이치', '제이'][i];
        const suffix = i % 2 === 0 ? '산업(주)' : '테크놀로지(주)';
        const companyName = i === 0 ? `(주)${category.slice(0,2)}텍엔지니어링` : `${prefix}${category.slice(0,2)}${suffix}`;
        
        return {
          id: 101 + i,
          name: companyName,
          specialty: `${category} 전문, 시스템 설계`,
          revenue: `${Math.floor(350 - i * 25)}억`,
          credit: i < 3 ? 'A0' : i < 7 ? 'BBB+' : 'B+',
          records: [`2024: ${category} 프로젝트 ${20-i}건`],
          region: `${region} 및 인근 지역`,
          licenses: [userLicense, '종합건설업', '기계설비'].slice(0, 3),
          phone: `0${i % 2 === 0 ? '2' : '31'}-${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`
        };
      });
      
      setDisplayVendors(newVendors);
      setIsSourcing(false);
    }, 2000);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} 
      animate={{ opacity: 1, y: 0 }} 
      exit={{ opacity: 0, y: 20 }}
      className="space-y-10"
    >
      {/* 1. 헤더 영역 */}
      <section>
        <div className="flex justify-between items-end mb-6 notranslate" translate="no">
          <div>
            <h2 className="text-3xl font-bold text-primary mb-2">AI 업체소싱 추천</h2>
            <p className="text-on-surface-variant text-sm">공신력 있는 데이터를 기반으로 한 최적의 파트너 매칭</p>
          </div>
          <div className="flex gap-2">
            <span className="px-3 py-1 bg-primary/10 border border-primary/20 text-primary text-[10px] font-bold rounded-full">매출 10억-1000억</span>
            <span className="px-3 py-1 bg-secondary/10 border border-secondary/20 text-secondary text-[10px] font-bold rounded-full">신용도 B+ 이상</span>
            <span className="px-3 py-1 bg-white/5 border border-white/10 text-slate-400 text-[10px] font-bold rounded-full">2024-2025 실적 보유</span>
          </div>
        </div>
      </section>

      {/* 2. AI 정밀 소싱 요청 섹션 (최상단으로 이동) */}
      <section className="bg-primary/5 rounded-[40px] p-1 border border-primary/10">
        <div className="glass-panel p-4 rounded-[38px] border border-white/5">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
              <Search size={20} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">AI 업체 소싱 요청</h3>
              <p className="text-[10px] text-on-surface-variant">구체적인 조건을 입력하시면 AI가 최적의 매칭 업체를 추천합니다.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="space-y-2">
              <label className="text-lg font-black text-primary uppercase tracking-tight ml-1">1. 필요공종</label>
              <input 
                type="text" 
                value={inputs.category}
                onChange={(e) => setInputs({...inputs, category: e.target.value})}
                placeholder="ex) 전기공사, 식품포장설비 등" 
                className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:ring-2 focus:ring-primary focus:outline-none transition-all placeholder:text-white/20"
              />
            </div>
            <div className="space-y-2">
              <label className="text-lg font-black text-primary uppercase tracking-tight ml-1">2. 지역</label>
              <input 
                type="text" 
                value={inputs.region}
                onChange={(e) => setInputs({...inputs, region: e.target.value})}
                placeholder="ex) 경기, 제주, 전국 등" 
                className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:ring-2 focus:ring-primary focus:outline-none transition-all placeholder:text-white/20"
              />
            </div>
            <div className="space-y-2">
              <label className="text-lg font-black text-primary uppercase tracking-tight ml-1">3. 보유면허</label>
              <input 
                type="text" 
                value={inputs.license}
                onChange={(e) => setInputs({...inputs, license: e.target.value})}
                placeholder="ex) 소방전기, 토목공사 등" 
                className="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:ring-2 focus:ring-primary focus:outline-none transition-all placeholder:text-white/20"
              />
            </div>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-3 border-t border-white/5">
            <div className="flex items-center gap-3 text-on-surface-variant">
              <ShieldCheck size={16} className="text-secondary" />
              <p className="text-[10px] leading-relaxed">
                입력하신 정보는 **AI 소싱 엔진**을 통해 국내 기업 신용 정보 및 <br/>
                조달청 실적 데이터와 실시간 매칭 분석을 진행합니다.
              </p>
            </div>
            <button 
              onClick={handleSourcing}
              disabled={isSourcing}
              className="w-full md:w-auto bg-primary text-on-primary px-8 py-3 rounded-xl font-bold text-sm hover:brightness-110 active:scale-95 transition-all shadow-xl shadow-primary/20 flex items-center justify-center gap-3 disabled:opacity-50"
            >
              {isSourcing ? (
                <>
                  <div className="animate-spin w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full" />
                  소싱 데이터 분석 중...
                </>
              ) : (
                <>
                  <Activity size={18} />
                  AI 소싱 분석 및 업체 매칭
                </>
              )}
            </button>
          </div>
        </div>
      </section>

      {/* 3. AI 추천 업체 리스트 */}
      <section className="space-y-6">
        <div className="flex items-center justify-between px-2">
          <h3 className="text-lg font-bold text-white flex items-center gap-3">
            AI 추천 업체 리스트 
            <span className="text-[10px] font-bold text-secondary bg-secondary/10 px-2 py-1 rounded-lg border border-secondary/20">Top 10 매칭 완료</span>
          </h3>
          <p className="text-[10px] text-on-surface-variant">업데이트: 2026.05.07</p>
        </div>

        <div className="grid grid-cols-1 gap-4">
          {displayVendors.map((v, idx) => (
            <div key={v.id || v.name} className="glass-card hover:border-primary/50 transition-all group relative overflow-hidden p-4 rounded-[24px]">
              <div className="absolute top-0 right-0 p-4">
                <div className="text-[9px] font-bold text-primary uppercase bg-primary/10 px-2 py-0.5 rounded-full border border-primary/20">Match Score: {99 - idx}%</div>
              </div>
              <div className="flex flex-col lg:flex-row gap-4">
                <div className="flex-[1.5] space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-[18px] bg-gradient-to-tr from-primary/20 to-secondary/20 flex items-center justify-center font-bold text-primary text-xl shadow-inner">
                      {v.name[0]}
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-on-surface notranslate" translate="no">{v.name}</h3>
                      <p className="text-xs text-secondary font-bold notranslate" translate="no">{v.specialty}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4 pt-2 border-t border-white/5">
                    <div className="notranslate" translate="no">
                      <p className="text-[9px] text-on-surface-variant font-bold uppercase mb-1">매출 규모</p>
                      <p className="text-xs font-bold text-on-surface">{v.revenue}</p>
                    </div>
                    <div className="notranslate" translate="no">
                      <p className="text-[9px] text-on-surface-variant font-bold uppercase mb-1">신용 등급</p>
                      <p className="text-xs font-bold text-primary">{v.credit}</p>
                    </div>
                    <div className="notranslate" translate="no">
                      <p className="text-[9px] text-on-surface-variant font-bold uppercase mb-1">활동 지역</p>
                      <p className="text-xs font-bold text-on-surface">{v.region}</p>
                    </div>
                    <div className="notranslate" translate="no">
                      <p className="text-[9px] text-on-surface-variant font-bold uppercase mb-1">연락처</p>
                      <p className="text-base font-bold text-secondary">{v.phone}</p>
                    </div>
                    <div className="flex flex-col gap-1">
                      <span className="text-[9px] text-on-surface/40 uppercase font-medium">보유 면허 (최대 3개)</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {v.licenses?.slice(0, 3).map((license, lIdx) => (
                          <span key={lIdx} className="text-[10px] bg-surface-variant/50 text-primary border border-primary/20 px-2 py-0.5 rounded-md font-bold">
                            {license}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex-1 bg-white/5 rounded-3xl p-6 border border-white/5 shadow-inner">
                  <p className="text-[10px] text-primary font-bold uppercase mb-4 flex items-center gap-2">
                    <Award size={14} /> 최근 2개년 주요 실적
                  </p>
                  <ul className="space-y-3">
                    {v.records.map((rec, i) => (
                      <li key={i} className="text-xs text-on-surface-variant flex items-start gap-3 notranslate" translate="no">
                        <div className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5 shrink-0" /> 
                        <span className="leading-relaxed">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </motion.div>
  );
};

// --- View 4: 구매 업무지식 (Business Knowledge FAQ) ---
const KnowledgeView = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');

  const faqs = [
    {
      q: "신규 업체 등록 시 필수 신용 등급 기준이 어떻게 되나요?",
      a: "당사 규정상 신용등급 B0 이상을 원칙으로 하며, 장기 계약의 경우 BBB- 이상을 권장합니다. B+ 미만 업체의 경우 보증보험 가입 등의 리스크 헷지 수단이 추가로 요구됩니다."
    },
    {
      q: "공인 표준 품셈 데이터는 언제 업데이트되나요?",
      a: "정부 공인 노임단가 및 품셈 데이터는 매년 상반기(1월)와 하반기(9월)를 기점으로 정기 업데이트됩니다. 본 시스템은 해당 데이터를 API로 실시간 연동하여 최신 분석 값을 제공합니다."
    },
    {
      q: "대금 지급 조건 중 기성금 지급 주기는 어떻게 되나요?",
      a: "일반적인 공사 및 용역의 경우 1개월 단위 기성을 원칙으로 합니다. 검수 완료 후 영업일 기준 15일 이내에 지급되며, 협력사 등급에 따라 상생결제 도입 등 유연한 조건 적용이 가능합니다."
    }
  ];

  const handleAsk = () => {
    if (!query) return;
    setLoading(true);
    
    // 구매 전문가용 고정밀 지식 엔진 (2026 정부 표준 + 사내 지침 통합)
    const knowledgeBase = [
      { 
        key: ['승인', '결재', '권한', '전결'], 
        ans: "[외부/정부 기준]: 상법 및 공정거래법상 위임전결권은 회사의 내부 통제 시스템(Internal Control)에 따라 정의됩니다.\n\n[내부/당사 지침]: 위임전결 규정 제7조(구매/계약 부문)\n- 50억 이상: 이사회/대표이사 승인\n- 10억 ~ 50억 미만: 사업본부장 승인\n- 1억 ~ 10억 미만: 구매실장 승인\n- 1억 미만: 구매팀장 전결\n*특이사항: 신규 업체 최초 계약 시에는 금액에 관계없이 실장급 이상의 승인이 필요합니다."
      },
      { 
        key: ['하도급', '외주', '지급보증', '연동제'], 
        ans: "[정부 공식 기준 (2026 개정 하도급법)]: \n- 지급보증: 2026년 개정안에 따라 1천만 원 이하 소액공사를 제외한 모든 건설 하도급 거래 시 '대금 지급보증'이 의무화되었습니다. (예외 사유 대폭 삭제)\n- 연동제: 주요 원재료뿐만 아니라 '에너지 비용(전기, 가스 등)'이 하도급대금의 10% 이상일 경우 반드시 연동제 대상에 포함해야 합니다.\n\n[내부/당사 관리]: 당사는 법 개정에 맞춰 모든 외주 계약 시 보증서 제출을 자동화하고 있으며, 에너지 비용 변동에 따른 계약금액 조정을 분기별로 시행하고 있습니다."
      },
      { 
        key: ['지체', '상금', '연체', '요율'], 
        ans: "[정부 공식 기준 (국가계약법 시행규칙 2026)]: \n- 공사: 0.05% / 물품 구매·제조: 0.075% / 용역: 0.125%\n- 한도: 지체상금 합계는 계약금액의 30%를 초과할 수 없습니다.\n\n[전문가 제언]: 당사 표준 계약서도 국가계약법 요율을 준용하고 있으나, 긴급 복구 자재 등 특수 목적의 경우 별도 특약을 통해 요율을 상향 조정할 수 있으므로 계약 체결 전 법무 검토가 필요합니다."
      },
      { 
        key: ['면허', '종합건설', '건산법', '자격'], 
        ans: "[정부 공식 기준 (건설산업기본법)]: \n- 종합건설업자 간 하도급은 원칙적 금지(제29조), 위반 시 1년 이하 영업정지 또는 과징금 대상입니다.\n- 반드시 해당 공종의 '전문건설 면허' 보유 업체와 계약해야 하며, 원도급 금액의 20% 이상 직접 시공 의무를 준수해야 합니다.\n\n[내부/당사 관리]: 당사 협력사 풀(Pool) 내의 종합/전문 면허 보유 현황은 실시간 KISCON 연동을 통해 검증되고 있습니다."
      },
      { 
        key: ['하자', '보증', 'AS', '수리'], 
        ans: "[정부 공식 기준 (국가계약법 및 민법)]: \n- 시설물/건축: 5~10년 / 기계/장치: 1~2년\n\n[내부/당사 지침]: 설비 구매 표준약관 제15조\n- 주요 설비: 검수일로부터 24개월 (하자이행보증보험 5% 제출 필수)\n- 일반 자재: 검수일로부터 12개월\n- 소모품: 6개월 또는 사용 주기 기준"
      },
      { 
        key: ['보존', '보관', '근거', '서류'], 
        ans: "[정부 공식 기준 (국세기본법 제85조)]: \n- 장부 및 증빙서류: 5년 보관 의무 (공공 조달은 10년 권고)\n\n[내부/당사 지침]: 문서관리 규정 제12조\n- 구매 계약서: 영구 보존\n- 견적/입찰/낙찰 서류: 10년 (전자결재 시스템 내 보관)\n- 검수/정산 증빙: 5년"
      },
      { 
        key: ['단순구매', '소액구매', 'MRO', '범위'], 
        ans: "[전문가 제언]: 조달청 '혁신제품'이나 2천만 원 이하 소액 물품은 수의계약이 가능한 것이 국가 표준이나, 당사 규정은 보다 엄격한 관리(500만 원 기준)를 택하고 있습니다.\n\n[내부/당사 지침]: 500만 원 이하 MRO 및 소모품은 법인카드 사용 후 사후 결의가 가능하며, 이는 공공 부문의 '클린카드' 운영 지침과 궤를 같이합니다."
      }
    ];

    setTimeout(() => {
      const cleanedQuery = query.replace(/\s/g, '');
      const matched = knowledgeBase.find(item => 
        item.key.some(k => cleanedQuery.includes(k) || query.includes(k))
      );
      
      let response = matched 
        ? matched.ans 
        : `질문하신 '${query}'에 대한 사내 규정은 현재 데이터베이스에 없으나, [국가법령정보센터] 및 [나라장터] 표준 지식에 근거하여 전문가 답변을 드립니다. \n\n[구매 전문가 코부장의 제언]: \n해당 사안은 일반적인 상거래 관례상 '신의성실의 원칙'에 따라 처리하되, 계약서상에 별도 명시가 없다면 국가계약법 표준 약관을 준용하는 것이 법적 리스크를 최소화하는 방법입니다. \n구체적인 조항 확인을 원하시면 핵심 키워드(하도급, 지체상금, 면허 등)를 포함해 다시 질문해 주세요.`;
      
      setAnswer(response);
      setLoading(false);
    }, 1200);
  };

  const handleReset = () => {
    setQuery('');
    setAnswer('');
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} 
      animate={{ opacity: 1, y: 0 }} 
      exit={{ opacity: 0, y: 20 }}
      className="space-y-10 pb-10"
    >
      <section>
        <h2 className="text-3xl font-bold text-primary mb-2">구매 업무지식 (AI FAQ)</h2>
        <p className="text-on-surface-variant text-sm">구매 프로세스 및 규정에 대한 실시간 지능형 답변</p>
      </section>

      {/* 챗봇 검색 인터페이스 */}
      <div className="glass-panel p-8 rounded-[40px] border border-primary/20 bg-primary/5 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 blur-[100px] rounded-full -mr-32 -mt-32"></div>
        <div className="relative z-10">
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="무엇이든 물어보세요 (예: 지체상금율, 하자담보 기간 등)" 
              className="flex-1 bg-surface-container-high border border-white/10 rounded-[20px] px-6 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary text-on-surface placeholder:text-on-surface/30 shadow-inner"
            />
            <button 
              onClick={handleReset}
              className="p-4 rounded-[20px] bg-white/5 border border-white/10 text-on-surface/60 hover:text-primary hover:bg-primary/10 transition-all active:scale-90"
              title="초기화"
            >
              <RotateCcw size={20} />
            </button>
            <button 
              onClick={handleAsk}
              disabled={loading}
              className="bg-primary text-on-primary px-8 py-4 rounded-[20px] font-black hover:brightness-110 active:scale-95 transition-all disabled:opacity-50 shadow-lg shadow-primary/20 flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-on-primary/30 border-t-on-primary rounded-full animate-spin"></div>
              ) : <Search size={20} />}
              질문하기
            </button>
          </div>

          {answer && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }} 
              animate={{ opacity: 1, scale: 1 }}
              className="p-6 bg-white/10 rounded-[30px] border border-primary/30 backdrop-blur-xl"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center shadow-lg">
                  <Bot size={18} className="text-on-primary" />
                </div>
                <div>
                  <p className="text-[10px] font-black text-primary uppercase tracking-tighter">Kodari AI Response</p>
                  <p className="text-[9px] text-on-surface/40 font-medium">분석 시간: 0.24s | 출처: 구매표준가이드 V2.1</p>
                </div>
              </div>
              <p className="text-sm leading-relaxed text-on-surface font-medium pr-4 whitespace-pre-wrap">{answer}</p>
            </motion.div>
          )}
        </div>
      </div>

      {/* 자주 묻는 질문 3종 (Chat Layout) */}
      <div className="space-y-6">
        <div className="flex items-center gap-3 px-2">
          <div className="w-1 h-6 bg-secondary rounded-full shadow-[0_0_8px_#4edea3]"></div>
          <h3 className="text-lg font-bold text-on-surface">자주 묻는 업무 지식 TOP 3</h3>
        </div>

        <div className="grid grid-cols-1 gap-8">
          {faqs.map((faq, idx) => (
            <div key={idx} className="space-y-4">
              {/* User Question */}
              <div className="flex justify-end">
                <div className="max-w-[80%] bg-surface-container-high px-5 py-3 rounded-[20px] rounded-tr-none border border-white/5 shadow-sm">
                  <p className="text-xs font-bold text-on-surface/80">{faq.q}</p>
                </div>
              </div>
              {/* AI Answer */}
              <div className="flex justify-start">
                <div className="max-w-[85%] bg-primary/10 px-6 py-4 rounded-[24px] rounded-tl-none border border-primary/20 relative">
                  <div className="absolute -left-1 top-0 w-3 h-3 bg-primary/20 blur-sm rounded-full"></div>
                  <div className="flex items-center gap-2 mb-2">
                    <Bot size={14} className="text-primary" />
                    <span className="text-[10px] font-black text-primary uppercase">Expert Answer</span>
                  </div>
                  <p className="text-xs leading-relaxed text-on-surface font-medium">{faq.a}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

// --- Main App ---
function App() {
  const [activeView, setActiveView] = useState('indicators');
  const [currency, setCurrency] = useState('USD');
  const [updateTime, setUpdateTime] = useState("");

  useEffect(() => {
    const calculateUpdateTime = () => {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      setUpdateTime(`${year}-${month}-${day} ${hours}:00`);
    };

    calculateUpdateTime();
    const interval = setInterval(calculateUpdateTime, 60000); // 1분마다 체크
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background text-on-background font-inter selection:bg-primary/30 selection:text-white pb-24">
      {/* Top App Bar */}
      <header className="sticky top-0 z-50 glass-panel border-b border-outline-variant px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20">
            <Activity className="text-background" size={24} />
          </div>
          <div className="notranslate" translate="no">
            <h1 className="text-xl font-bold font-space bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">비용 분석 시스템</h1>
            <p className="text-[10px] text-on-surface-variant uppercase tracking-widest font-bold">지능형 구매 분석 시스템 v2.0</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="hidden md:flex flex-col items-end">
            <span className="text-[10px] font-bold text-primary uppercase">3031-Secure-Node</span>
            <span className="text-[10px] text-on-surface-variant">Last Update: Just Now</span>
          </div>
          <button className="relative p-2 rounded-full hover:bg-white/5 transition-all active:scale-90">
            <Bell size={20} className="text-on-surface-variant" />
            <span className="absolute top-2 right-2 w-2 h-2 bg-error rounded-full border-2 border-background"></span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 pt-8">
        <AnimatePresence mode="wait">
          {activeView === 'indicators' && <DashboardView key="indicators" currency={currency} setCurrency={setCurrency} updateTime={updateTime} />}
          {activeView === 'standard' && <CostStandardView key="standard" />}
          {activeView === 'vendors' && <SourcingView key="vendors" />}
          {activeView === 'knowledge' && <KnowledgeView key="knowledge" />}
        </AnimatePresence>
      </main>

      {/* Bottom Navigation Bar */}
      <nav className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 px-2 py-2 glass-panel border border-outline-variant rounded-full flex gap-1 shadow-2xl shadow-black/50">
        {[
          { id: 'indicators', label: '지표', icon: LayoutDashboard },
          { id: 'standard', label: '품셈분석', icon: LineChart },
          { id: 'vendors', label: '업체소싱', icon: Users },
          { id: 'knowledge', label: '업무지식', icon: BookOpen },
        ].map((item) => {
          const Icon = item.icon;
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-full transition-all duration-300 relative overflow-hidden group ${
                isActive ? 'bg-primary text-background shadow-lg shadow-primary/30' : 'text-on-surface-variant hover:text-on-surface'
              }`}
            >
              <Icon size={18} className={isActive ? 'animate-pulse' : 'group-hover:scale-110 transition-transform'} />
              <span className={`text-xs font-bold ${isActive ? 'block' : 'hidden md:block opacity-60'}`}>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Background Decoration */}
      <div className="fixed inset-0 pointer-events-none -z-10 opacity-20 overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 blur-[120px] rounded-full"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 blur-[120px] rounded-full"></div>
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-soft-light"></div>
      </div>
    </div>
  );
}

export default App;
