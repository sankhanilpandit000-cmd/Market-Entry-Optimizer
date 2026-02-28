import React, { useMemo } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Activity, TrendingUp, TrendingDown, Minus, Calendar, Target, AlertCircle, CheckCircle2, PieChart, Users, Lightbulb, Zap, Sparkles, Flame, Rocket, Award } from 'lucide-react';
import { MarketAnalysisResult } from '../services/geminiService';
import { motion } from 'motion/react';

interface DashboardProps {
  data: MarketAnalysisResult;
}

export function Dashboard({ data }: DashboardProps) {
  // DYNAMIC TREND DATA GENERATION
  const chartData = useMemo(() => {
    if (!data.trendData || data.trendData.length === 0) {
      const baseValue = Math.min(data.successProbability, data.readinessScore);
      return Array.from({ length: 12 }, (_, i) => {
        const month = i + 1;
        const variance = Math.sin(month * 0.5) * 15;
        const growth = (month / 12) * 20;
        const value = Math.max(10, Math.min(100, baseValue + variance + growth));
        
        return {
          month: `M${month}`,
          favorability: Math.round(value),
        };
      });
    }
    return data.trendData;
  }, [data.trendData, data.successProbability, data.readinessScore]);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-emerald-400" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-pink-400" />;
      default: return <Minus className="w-4 h-4 text-indigo-300" />;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return 'from-emerald-400 to-teal-500';
    if (score >= 50) return 'from-amber-400 to-orange-500';
    return 'from-pink-400 to-rose-500';
  };

  const getScoreBgClass = (score: number) => {
    if (score >= 75) return 'from-emerald-500/20 to-teal-500/20 border-emerald-400/50';
    if (score >= 50) return 'from-amber-500/20 to-orange-500/20 border-amber-400/50';
    return 'from-pink-500/20 to-rose-500/20 border-pink-400/50';
  };

  const getThreatColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'high': return 'from-pink-500/30 to-rose-500/30 border-pink-400/60 text-pink-200';
      case 'medium': return 'from-amber-500/30 to-orange-500/30 border-amber-400/60 text-amber-200';
      case 'low': return 'from-emerald-500/30 to-teal-500/30 border-emerald-400/60 text-emerald-200';
      default: return 'from-slate-500/30 to-slate-600/30 border-slate-400/60 text-slate-200';
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact?.toLowerCase()) {
      case 'high': return 'from-blue-500/30 to-cyan-500/30 border-blue-400/60 text-blue-200';
      case 'medium': return 'from-indigo-500/30 to-purple-500/30 border-indigo-400/60 text-indigo-200';
      case 'low': return 'from-violet-500/30 to-fuchsia-500/30 border-violet-400/60 text-violet-200';
      default: return 'from-slate-500/30 to-slate-600/30 border-slate-400/60 text-slate-200';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-6 md:p-10 overflow-hidden relative">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full opacity-10 blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full opacity-10 blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-gradient-to-br from-indigo-500 to-emerald-500 rounded-full opacity-5 blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-7xl mx-auto space-y-8 relative z-10"
      >
        {/* Header Section */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="w-8 h-8 text-cyan-400" />
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-300 via-blue-300 to-purple-300 bg-clip-text text-transparent">
              Market Intelligence Dashboard
            </h1>
          </div>
          <p className="text-slate-400 text-lg">Real-time analysis powered by advanced AI</p>
        </motion.div>

        {/* Top Row: Key Metrics with Glass Morphism */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Readiness Score */}
          <motion.div 
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className={`backdrop-blur-xl bg-gradient-to-br ${getScoreBgClass(data.readinessScore)} border rounded-3xl p-8 shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300 hover:scale-105 cursor-pointer group relative overflow-hidden`}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 transition-opacity duration-300" />
            
            <div className="flex items-center justify-between mb-6 relative z-10">
              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest">📈 Market Readiness</h3>
              <Activity className="w-6 h-6 text-cyan-400 drop-shadow-lg" />
            </div>
            
            <div className="relative z-10 mb-6">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, duration: 0.6, type: 'spring' }}
                className="flex items-baseline gap-3"
              >
                <span className={`text-6xl font-black bg-gradient-to-r ${getScoreColor(data.readinessScore)} bg-clip-text text-transparent`}>
                  {data.readinessScore}
                </span>
                <span className="text-xl text-slate-400 font-semibold">/100</span>
              </motion.div>
            </div>
            
            <div className="relative z-10 w-full bg-slate-800/50 rounded-full h-2 overflow-hidden border border-slate-700/50">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${data.readinessScore}%` }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.5 }}
                className={`h-full rounded-full bg-gradient-to-r ${getScoreColor(data.readinessScore)} shadow-lg shadow-current`}
              />
            </div>
            
            <p className="text-xs text-slate-400 mt-4 relative z-10">Optimized for market entry</p>
          </motion.div>

          {/* Success Probability */}
          <motion.div 
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className={`backdrop-blur-xl bg-gradient-to-br ${getScoreBgClass(data.successProbability)} border rounded-3xl p-8 shadow-2xl hover:shadow-pink-500/20 transition-all duration-300 hover:scale-105 cursor-pointer group relative overflow-hidden`}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 transition-opacity duration-300" />
            
            <div className="flex items-center justify-between mb-6 relative z-10">
              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest">🎯 Success Rate</h3>
              <PieChart className="w-6 h-6 text-pink-400 drop-shadow-lg" />
            </div>
            
            <div className="relative z-10 mb-6">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.5, duration: 0.6, type: 'spring' }}
                className="flex items-baseline gap-3"
              >
                <span className={`text-6xl font-black bg-gradient-to-r ${getScoreColor(data.successProbability)} bg-clip-text text-transparent`}>
                  {data.successProbability}%
                </span>
              </motion.div>
            </div>
            
            <div className="relative z-10 w-full bg-slate-800/50 rounded-full h-2 overflow-hidden border border-slate-700/50">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${data.successProbability}%` }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.6 }}
                className={`h-full rounded-full bg-gradient-to-r ${getScoreColor(data.successProbability)} shadow-lg shadow-current`}
              />
            </div>
            
            <p className="text-xs text-slate-400 mt-4 relative z-10">Probability of successful launch</p>
          </motion.div>

          {/* Optimal Window */}
          <motion.div 
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="backdrop-blur-xl bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-purple-400/50 rounded-3xl p-8 shadow-2xl hover:shadow-purple-500/20 transition-all duration-300 hover:scale-105 cursor-pointer group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 transition-opacity duration-300" />
            
            <div className="flex items-center justify-between mb-6 relative z-10">
              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest">📅 Launch Window</h3>
              <Calendar className="w-6 h-6 text-purple-400 drop-shadow-lg" />
            </div>
            
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.6, duration: 0.6, type: 'spring' }}
              className="relative z-10"
            >
              <div className="text-5xl font-black bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent mb-3">
                {data.optimalLaunchWindow}
              </div>
              <p className="text-slate-300 text-sm leading-relaxed">
                {data.summary}
              </p>
            </motion.div>
          </motion.div>
        </div>

        {/* Middle Row: Chart & Factors */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Trend Chart */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.5 }}
            className="backdrop-blur-xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-blue-400/30 rounded-3xl p-8 shadow-2xl lg:col-span-2 overflow-hidden relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-transparent to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="flex items-center justify-between mb-8 relative z-10">
              <h3 className="text-xl font-bold text-transparent bg-gradient-to-r from-blue-300 to-cyan-300 bg-clip-text uppercase tracking-widest">📊 12-Month Projection</h3>
              <Rocket className="w-6 h-6 text-blue-400 drop-shadow-lg" />
            </div>
            
            <div className="h-[350px] w-full relative z-10">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart 
                  data={chartData}
                  margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
                  key={JSON.stringify(chartData)}
                >
                  <defs>
                    <linearGradient id="colorFavorability" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.4}/>
                      <stop offset="100%" stopColor="#0ea5e9" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="shimmer" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#transparent"/>
                      <stop offset="50%" stopColor="#ffffff" stopOpacity="0.3"/>
                      <stop offset="100%" stopColor="#transparent"/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.3} />
                  <XAxis 
                    dataKey="month" 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{ fontSize: 12, fill: '#cbd5e1', fontWeight: 500 }} 
                    dy={10}
                  />
                  <YAxis 
                    axisLine={false} 
                    tickLine={false} 
                    tick={{ fontSize: 12, fill: '#cbd5e1', fontWeight: 500 }}
                    domain={[0, 100]}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      borderRadius: '12px', 
                      border: '2px solid #0ea5e9',
                      boxShadow: '0 20px 25px -5px rgba(6, 182, 212, 0.3)',
                      backgroundColor: '#0f172a',
                      padding: '12px 16px'
                    }}
                    itemStyle={{ color: '#06b6d4', fontWeight: 700, fontSize: '14px' }}
                    labelStyle={{ color: '#cbd5e1', fontWeight: 600 }}
                    formatter={(value: any) => [`${value}`, 'Favorability']}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="favorability" 
                    stroke="#06b6d4" 
                    strokeWidth={3}
                    dot={{ fill: '#06b6d4', r: 4 }}
                    activeDot={{ r: 7, fill: '#00d9ff' }}
                    fillOpacity={1} 
                    fill="url(#colorFavorability)" 
                    isAnimationActive={true}
                    animationDuration={800}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Key Factors */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="backdrop-blur-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-400/30 rounded-3xl p-8 shadow-2xl flex flex-col overflow-hidden relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-transparent to-teal-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="flex items-center justify-between mb-6 relative z-10">
              <h3 className="text-lg font-bold text-transparent bg-gradient-to-r from-emerald-300 to-teal-300 bg-clip-text uppercase tracking-widest">⚡ Key Factors</h3>
              <Award className="w-6 h-6 text-emerald-400 drop-shadow-lg" />
            </div>
            
            <div className="flex-1 overflow-y-auto pr-2 space-y-3 max-h-[350px] scrollbar-hide relative z-10">
              {data.factors && data.factors.map((factor, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, x: -15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + idx * 0.1 }}
                  className="p-4 rounded-2xl border border-slate-600/50 bg-gradient-to-br from-slate-700/50 to-slate-800/30 hover:border-emerald-400/50 transition-all duration-300 group/factor"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-slate-100 text-sm group-hover/factor:text-emerald-300 transition-colors">{factor.name}</span>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-black px-3 py-1 rounded-full bg-gradient-to-r ${getScoreColor(factor.score)} text-slate-900 drop-shadow-lg`}>
                        {factor.score}%
                      </span>
                      {getTrendIcon(factor.trend)}
                    </div>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {factor.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Market Gaps & Competitors */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Market Gaps */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.5 }}
            className="backdrop-blur-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-400/30 rounded-3xl p-8 shadow-2xl relative group overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-transparent to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <Target className="w-6 h-6 text-blue-400 drop-shadow-lg" />
              <h3 className="text-lg font-bold text-transparent bg-gradient-to-r from-blue-300 to-cyan-300 bg-clip-text uppercase tracking-widest">Market Gaps</h3>
            </div>
            
            <ul className="space-y-3 relative z-10">
              {data.marketGaps && data.marketGaps.map((gap, idx) => (
                <motion.li 
                  key={idx}
                  initial={{ opacity: 0, x: -15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                  className="flex items-start gap-4 p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 hover:border-blue-400/50 transition-all duration-300 group/gap"
                >
                  <div className="flex-shrink-0 w-2 h-2 rounded-full bg-gradient-to-r from-blue-400 to-cyan-400 mt-2 drop-shadow-lg" />
                  <p className="text-sm text-slate-200 leading-relaxed group-hover/gap:text-slate-100 transition-colors">{gap}</p>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Competitors */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.5 }}
            className="backdrop-blur-xl bg-gradient-to-br from-pink-500/20 to-rose-500/20 border border-pink-400/30 rounded-3xl p-8 shadow-2xl relative group overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-pink-500/5 via-transparent to-rose-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <Users className="w-6 h-6 text-pink-400 drop-shadow-lg" />
              <h3 className="text-lg font-bold text-transparent bg-gradient-to-r from-pink-300 to-rose-300 bg-clip-text uppercase tracking-widest">Competitors</h3>
            </div>
            
            <div className="space-y-3 relative z-10">
              {data.competitors && data.competitors.map((comp, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, x: -15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + idx * 0.1 }}
                  className={`p-4 rounded-xl border backdrop-blur-sm bg-gradient-to-br ${getThreatColor(comp.threatLevel)} transition-all duration-300 group/comp hover:scale-105`}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <Flame className="w-4 h-4 flex-shrink-0" />
                    <span className="font-bold text-sm">{comp.name}</span>
                    <span className="ml-auto text-[11px] font-black uppercase px-2.5 py-1 rounded-full bg-slate-900/50 border border-slate-700">
                      {comp.threatLevel}
                    </span>
                  </div>
                  <p className="text-xs leading-relaxed opacity-90">{comp.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Innovations */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9, duration: 0.5 }}
          className="backdrop-blur-xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-400/30 rounded-3xl p-8 shadow-2xl relative group overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-amber-500/5 via-transparent to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          <div className="flex items-center gap-3 mb-8 relative z-10">
            <Lightbulb className="w-6 h-6 text-amber-400 drop-shadow-lg" />
            <h3 className="text-xl font-bold text-transparent bg-gradient-to-r from-amber-300 to-orange-300 bg-clip-text uppercase tracking-widest">Innovations</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative z-10">
            {data.innovations && data.innovations.map((inv, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 15, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ delay: 0.9 + idx * 0.15 }}
                whileHover={{ scale: 1.05, y: -5 }}
                className={`p-6 rounded-2xl border backdrop-blur-sm bg-gradient-to-br ${getImpactColor(inv.impact)} group/innovation transition-all duration-300 overflow-hidden relative`}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover/innovation:opacity-10 transition-opacity duration-300" />
                
                <div className="relative z-10 flex items-start justify-between mb-4">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-sm flex items-center justify-center border border-white/30">
                    <Zap className="w-5 h-5 text-white drop-shadow-lg" />
                  </div>
                  <span className="text-[10px] font-black uppercase px-2.5 py-1 rounded-lg bg-slate-900/60 border border-slate-700/50">
                    {inv.impact}
                  </span>
                </div>
                
                <h4 className="font-bold text-slate-100 text-sm mb-3 group-hover/innovation:text-white transition-colors">{inv.title}</h4>
                <p className="text-xs leading-relaxed opacity-90">{inv.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Recommendations */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="backdrop-blur-xl bg-gradient-to-br from-emerald-500/20 to-green-500/20 border border-emerald-400/30 rounded-3xl p-8 shadow-2xl relative group overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-transparent to-green-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          <div className="flex items-center gap-3 mb-8 relative z-10">
            <CheckCircle2 className="w-6 h-6 text-emerald-400 drop-shadow-lg" />
            <h3 className="text-xl font-bold text-transparent bg-gradient-to-r from-emerald-300 to-green-300 bg-clip-text uppercase tracking-widest">Recommendations</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 relative z-10">
            {data.recommendations && data.recommendations.map((rec, idx) => (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + idx * 0.1 }}
                whileHover={{ y: -3 }}
                className="flex items-start gap-4 p-5 rounded-2xl bg-gradient-to-br from-slate-800/60 to-slate-700/40 border border-slate-600/50 hover:border-emerald-400/50 transition-all duration-300 group/rec"
              >
                <motion.div 
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 1 + idx * 0.1 + 0.2, type: 'spring' }}
                  className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-green-500 flex items-center justify-center text-slate-900 font-bold text-sm drop-shadow-lg"
                >
                  {idx + 1}
                </motion.div>
                <p className="text-sm text-slate-200 leading-relaxed group-hover/rec:text-slate-100 transition-colors mt-0.5">
                  {rec}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}

export default Dashboard;
