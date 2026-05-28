import React, { useState, useEffect } from 'react';

// --- Shared Components ---

const TopAppBar = () => (
  <header className="bg-[#B7EEDB] dark:bg-slate-900 fixed top-0 w-full z-50 border-b-4 border-[#9BD2BF] shadow-sm">
    <div className="flex justify-between items-center w-full px-6 py-4 max-w-screen-xl mx-auto">
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="w-12 h-12 rounded-full border-4 border-white shadow-sm overflow-hidden bg-white">
            <img 
              className="w-full h-full object-cover" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKPScLHnYOazqSCRMT0_JGDB-fGp7x94yFZEypVc04Pz52huUruQVRG9irLaUvajeXMxI_yQhuQ_bMpknGAXZmg1nS3E133_jrIWskW1KKJjwjy4-RBYNDRwbGgUk-YD88Sn9Y7wLPcWpZ6y1NFZMWwZUO0nnsEJNRWOvwEyt42JGiEJGf9XFTmaBnMjtEWoGHoCf79EyLmdG08RaL9Ae31MHDDmPy462fIqO7aRrhHX-oJJXvfoHOM5aXkiWdMcEa3LOnkgwctWbG" 
              alt="Avatar"
            />
          </div>
          <div className="absolute -bottom-1 -right-1 bg-[#E7C269] text-on-secondary-fixed text-[10px] font-bold px-1.5 py-0.5 rounded-full border-2 border-white shadow-sm">
            Lv.12
          </div>
        </div>
        <div className="flex flex-col">
          <h1 className="text-[19px] font-black text-[#194F42] leading-tight font-headline-md">Novice Gourmet</h1>
          <span className="text-[10px] font-extrabold text-[#194F42]/60 uppercase tracking-[0.2em]">Spring Season</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button className="text-[#194F42] p-2 hover:bg-white/20 rounded-full transition-colors active:translate-y-[2px]">
          <span className="material-symbols-outlined text-2xl">military_tech</span>
        </button>
      </div>
    </div>
    <div className="bg-[#765B06] text-white py-1 overflow-hidden border-b-2 border-black/10">
      <div className="max-w-screen-xl mx-auto flex items-center px-6">
        <div className="flex items-center gap-2 bg-[#FFDF96] text-[#251A00] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter mr-4 z-10 shrink-0">
          <span className="material-symbols-outlined text-[14px] filled-icon">campaign</span> LIVE
        </div>
        <div className="relative flex-1 overflow-hidden h-5">
          <div className="ticker-scroll font-label-sm flex gap-12 text-[12px] font-bold">
            <span>Gyeongju: Fresh spring strawberries spotted at the central market! 🍓</span>
            <span>Jeju: Hallabong season is at its peak! 🍊</span>
            <span>Hadong: First flush green tea leaves are ready for harvest! 🍃</span>
          </div>
        </div>
      </div>
    </div>
  </header>
);

const BottomNavBar = ({ activeView, setView }) => {
  const navItems = [
    { id: 'home', icon: 'home', label: 'Home' },
    { id: 'collection', icon: 'inventory_2', label: 'Collection' },
    { id: 'camera', icon: 'photo_camera', label: 'Camera' },
    { id: 'community', icon: 'group', label: 'Community' },
  ];

  return (
    <nav className="bg-white dark:bg-slate-950 fixed bottom-0 left-0 w-full z-50 border-t-4 border-[#F2F4F3] rounded-t-[32px] shadow-[0_-4px_16px_rgba(0,0,0,0.04)]">
      <div className="flex justify-around items-end w-full px-4 pb-6 pt-2 max-w-screen-xl mx-auto">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setView(item.id)}
            className={`flex flex-col items-center justify-center px-5 py-2 transition-all duration-150 ${
              activeView === item.id 
                ? 'text-[#346859] rounded-[20px] translate-y-[-6px] active:scale-95' 
                : 'text-[#C0C9C4] hover:text-[#346859] active:scale-95'
            }`}
          >
            <span className={`material-symbols-outlined text-[28px] ${activeView === item.id ? 'filled-icon' : ''}`}>
              {item.icon}
            </span>
            <span className="text-[10px] font-black uppercase tracking-widest mt-1">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

// --- Views ---

const HomeView = () => (
  <main className="pb-32 px-6 max-w-screen-xl mx-auto pt-40 animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
    {/* Adventure Progress Card */}
    <section className="tile-card tile-surface p-8">
      <div className="mb-6">
        <h2 className="text-[14px] font-bold text-outline uppercase tracking-wider mb-2">Adventure Progress</h2>
        <p className="text-[16px] font-medium text-on-surface-variant">
          You're 240 XP away from becoming a <span className="text-primary font-bold border-b-2 border-primary/30">Seasonal Sous-Chef</span>!
        </p>
      </div>
      
      <div className="relative h-12 w-full flex items-center px-2">
        <div className="flex justify-between w-full absolute -top-1 px-1">
          <span className="text-[12px] font-bold text-outline">Level 12</span>
          <span className="text-[12px] font-bold text-outline">Level 13</span>
        </div>
        <div className="h-4 w-full bg-[#E9E8E5] rounded-full overflow-hidden p-0.5">
          <div className="h-full bg-[#346859] rounded-full relative" style={{ width: '75%' }}></div>
        </div>
        {/* Progress Icons exactly as in image */}
        <div className="absolute inset-0 flex items-center justify-around pointer-events-none px-12">
          <span className="material-symbols-outlined text-secondary text-[20px] filled-icon translate-y-1">energy_savings_leaf</span>
          <span className="material-symbols-outlined text-secondary text-[20px] filled-icon translate-y-1">local_florist</span>
          <span className="material-symbols-outlined text-secondary text-[20px] filled-icon translate-y-1">grade</span>
        </div>
      </div>
    </section>

    {/* Recipes Mastered Card */}
    <section className="tile-card tile-secondary bg-[#FFDF96] p-8 flex flex-col items-center text-center gap-4">
      <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-inner">
        <span className="material-symbols-outlined text-[#765B06] text-[32px] filled-icon">restaurant</span>
      </div>
      <div>
        <h3 className="text-[20px] font-black text-[#765B06]">14 Recipes</h3>
        <p className="text-[13px] font-bold text-[#765B06]/70 uppercase">Mastered this Season</p>
      </div>
      <button className="mt-2 px-8 py-2.5 bg-white rounded-[16px] font-black text-[#765B06] shadow-sm active:translate-y-1 transition-all text-[14px]">
        View Log
      </button>
    </section>

    {/* Daily Quests Section */}
    <section>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[18px] font-black text-on-surface">Daily Quests</h2>
        <span className="bg-[#FFDAD6] text-[#93000A] text-[11px] font-black px-2.5 py-1 rounded-[10px]">2h Left</span>
      </div>
      <div className="space-y-3">
        {[
          { title: 'Catch the Spring Strawberry', desc: 'Find local farm varieties', icon: 'shopping_basket', bg: 'bg-[#B7EEDB]', color: 'text-[#194F42]', status: 'circle' },
          { title: 'Taste the Spring Sea Bream', desc: 'Identify Sakura Tai texture', icon: 'set_meal', bg: 'bg-[#FFDAD7]', color: 'text-[#874F4C]', status: 'check' },
          { title: 'Gather Wild Herbs', desc: 'Unlock at Lv. 15', icon: 'bakery_dining', bg: 'bg-[#F2F4F3]', color: 'text-outline', status: 'lock' },
        ].map((quest, i) => (
          <div key={i} className={`tile-card tile-surface p-5 flex items-center gap-4 ${quest.status === 'lock' ? 'opacity-60' : ''}`}>
            <div className={`w-14 h-14 ${quest.bg} rounded-[18px] flex items-center justify-center shadow-sm`}>
              <span className={`material-symbols-outlined text-[28px] ${quest.color}`}>{quest.icon}</span>
            </div>
            <div className="flex-1">
              <h4 className="text-[15px] font-bold text-on-surface">{quest.title}</h4>
              <p className="text-[12px] font-medium text-outline italic">{quest.desc}</p>
            </div>
            <span className={`material-symbols-outlined text-outline ${quest.status === 'check' ? 'text-primary' : ''}`}>
              {quest.status === 'circle' ? 'radio_button_unchecked' : quest.status === 'check' ? 'check_circle' : 'lock'}
            </span>
          </div>
        ))}
      </div>
    </section>
  </main>
);

const CollectionView = () => (
  <main className="max-w-screen-xl mx-auto pt-40 px-6 pb-32 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <section className="mb-8">
      <h2 className="text-[20px] font-black text-primary mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined filled-icon">stars</span> Mastery Badges
      </h2>
      <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
        {[
          { title: 'Strawberry Master', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA0o-9zOu7TzKCAz2WOfZyq_X83Ew3krQ58R_5O8N7A78xS5ygZu64LJXnHivw-E1L3eCXRi9XzBHBy2u7jhq0RP8ZnyjFmKmP98W0emoBhgoW8hwRNfO_VPkNmxvXH5jLu59y9260O3VK48dnfKFNhqtTNLHlK8uIexbPRNO7RrFGMIs3n8UmcQyD87oH4zO9FPSoavqmGHeUVCNPkicIDzaNjaACVwiUlA75FZfis97NAZ_28-nwRDfx_T_ZstNTaT62QHg7JGlaV', bg: 'bg-[#FFDF96]', border: 'tile-secondary' },
          { title: 'Spring Messenger', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC_ssRJnBO7Pl-roCrGzjz_U9f2Sw2JjdLrHGKcWue78A-QJgKy3oZsSaAosCRIFWCEbr8yDDfzeK6kAitXPhq7f-QtGJSQiP8NUsP0IPYUduuPObTE7mSGTuozc-HG8mH8hrBFPIHL_LI7l0haqWAu3jVjMDxlrrGSFOy_jZ84FnPfEGcL7G0uzBP6LOiuhNDU2pPGaI-Za7ttVu9OGmmnMWcyRz5r4OMlE34BAHsvSWByCkzbzHxfZJs84VY9giGI7dhi06WDQ99t', bg: 'bg-[#B7EEDB]', border: 'tile-primary' },
        ].map((badge, i) => (
          <div key={i} className={`flex-shrink-0 flex flex-col items-center ${badge.bg} p-5 rounded-[24px] tile-card ${badge.border} min-w-[140px]`}>
            <div className="w-16 h-16 mb-2">
              <img src={badge.img} className="w-full h-full object-contain" alt={badge.title} />
            </div>
            <span className="text-[13px] font-bold text-on-surface">{badge.title}</span>
          </div>
        ))}
      </div>
    </section>

    <nav className="flex gap-2 mb-6 bg-[#E9E8E5] p-1.5 rounded-[20px] overflow-x-auto no-scrollbar">
      {['Fruits', 'Seafood', 'Vegetables'].map((cat, i) => (
        <button key={i} className={`px-8 py-2 rounded-[14px] text-[13px] font-black transition-all ${i === 0 ? 'bg-[#346859] text-white shadow-sm' : 'text-outline hover:bg-white/50'}`}>
          {cat}
        </button>
      ))}
    </nav>

    <div className="grid grid-cols-2 gap-4">
      {[
        { name: 'Shine Muscat', date: 'Oct 12', rarity: 'RARE', bg: 'bg-white', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDN4zN3rXq7pfRKCuIpWFIswRK2s72kWMydAJz7fjQID13-kG1iPsXx-bkoxHWtLy0LfWIVqv_zMgob0GqpkgSXuqPIndQnqqAJGokyDvLYwiCnrYgf9s9YkrSYtmEltlYFpNQrPudRvl48utRp3FGfuS7KU_nfpzs4WM_cSMh87A_xsCcYuBe5Yy_QXyeHkNxHavxOrHTbqPTItCpXd-VGKybvVZ7nPFizwIp17wW0aGoQly14RLDu4fIdiH8lLiljDubuyz9b7d18', collected: true },
        { name: 'King Crab', date: 'Nov 05', rarity: 'SEASONAL', bg: 'bg-white', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDzP_VxTURJ602Rxro7YqkszBh3SM3IB3713aOI5YS-l7O3Yscjm811V2ZAlMPfTEMSdQWZ02b56jMq3DTu9H_tj3xHZOnhC1LJZv0-6FI6CtfGM71gJM79y-45cGc0EITIGCPGxLd_XLpfb-0HhG9AasXUilLWcei4DNHIGVEjQEPq9AlEaBdPeqcTd8WOXItkQKhF0y_POFcrgPSxbqymF9FfalqdSlTRPmFJazHF2cOZGP8DEmFNu9xIrG9XtDgTlPYJMwAwbmzU', collected: true },
        { name: 'Undiscovered', rarity: 'Unknown', bg: 'bg-[#E9E8E5]', icon: 'question_mark', locked: true },
        { name: 'Premium Sake', date: 'Sep 28', rarity: 'COMMON', bg: 'bg-white', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD4wJ9ALkXLDOelldZu866YrAGHwQrUXiXPh2zcFR1kcjXslwRXa5X8m5Cqqau26OdKjwBmcSN-1ODlj3b1CbdACvxo7oxV100EFnP3y0wVN_89Ph3VlrHdrPLTrPLJqjiX36DCyyuTSr6UlvDYmGWMr35YlZ4blfPEh9y_laXdjR74V5ADRHNdMB6ma_hCVMLOM-NR_q67HVmxj0F2GqYFsn7BU4vl1dZwo3s35RK2SbkHRziQGhMnDs7OvYft56QYmYym2mwqgdPw', collected: true },
      ].map((item, i) => (
        <article key={i} className={`tile-card tile-surface overflow-hidden group ${item.locked ? 'bg-[#E9E8E5] border-dashed border-2 opacity-60' : ''}`}>
          <div className="relative aspect-square p-4 bg-[#F8F9F8] flex items-center justify-center">
            {item.img ? <img src={item.img} className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-300" alt={item.name} /> : <span className="material-symbols-outlined text-[#C0C9C4] text-[64px]">{item.icon}</span>}
            {item.collected && (
              <div className="absolute top-2 right-2 bg-[#765B06] rounded-full p-1 border-2 border-white">
                <span className="material-symbols-outlined text-white text-[12px] filled-icon">verified</span>
              </div>
            )}
          </div>
          <div className="p-4 bg-white">
            <div className="flex justify-between items-start mb-1">
              <h3 className="text-[15px] font-black text-on-surface">{item.name}</h3>
              {!item.locked && <span className={`text-[9px] font-black px-1.5 py-0.5 rounded-[4px] ${item.rarity === 'RARE' ? 'bg-[#FFDF96] text-[#765B06]' : item.rarity === 'SEASONAL' ? 'bg-[#B7EEDB] text-[#194F42]' : 'bg-[#E9E8E5] text-outline'}`}>{item.rarity}</span>}
            </div>
            {!item.locked && (
              <div className="flex items-center gap-1 mt-2 text-[#C0C9C4]">
                <span className="material-symbols-outlined text-[14px]">calendar_today</span>
                <p className="text-[9px] font-black uppercase">Collected: {item.date}</p>
              </div>
            )}
          </div>
        </article>
      ))}
    </div>
  </main>
);

const CommunityView = () => (
  <main className="pt-40 px-6 max-w-screen-xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-32">
    <section>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[22px] font-black text-on-surface">Hot Places</h2>
        <span className="text-[12px] font-black text-primary uppercase border-b-2 border-primary/30 tracking-widest cursor-pointer">View Map</span>
      </div>
      <div className="space-y-4">
        {/* Large Card exactly as image */}
        <div className="relative h-[240px] rounded-[32px] overflow-hidden tile-card tile-surface">
          <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDvAq2d822F_igIZ2blejVWY3Y3_EJ5_zQl-wAc3e25wbCKwNrqhlJCAUGTalKXWB5dXKbuDdthuRdnfWl50op3NJT62h8Lme4s8KInJC_T951gVP3jZ_1ybjL1Hukj_NgwXUshepGvs7KnmQ5ldG-p8REOJ6Cdlrc353tuIAClx7gShxpGE-z0sXwtaRyQLQmxhO-whq6xGHrREj9mkGQxB1LMCEvvjjnDm2X7BCVXkhF6C-9kUuwHYKaEr0OBFkB8tspkGVK3xBdS" alt="Map" />
          <div className="absolute inset-x-4 bottom-4 bg-white/90 backdrop-blur-md p-5 rounded-[24px] border-b-4 border-emerald-100 shadow-lg">
            <h3 className="text-[18px] font-black text-[#194F42]">Autumnal Orchards</h3>
            <div className="flex items-center gap-2 text-primary">
              <span className="material-symbols-outlined text-[16px]">location_on</span>
              <span className="text-[12px] font-bold">North Valley, Kyoto</span>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-1 gap-4">
          <div className="tile-card tile-secondary bg-[#FFDF96] p-5 flex items-center gap-4">
            <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-sm">
              <span className="material-symbols-outlined text-[#765B06] filled-icon">bakery_dining</span>
            </div>
            <div>
              <p className="font-black text-[#765B06] text-[15px]">Sugar Bloom</p>
              <p className="text-[12px] font-bold text-[#765B06]/60">Rare Pastries</p>
            </div>
          </div>
          <div className="tile-card tile-tertiary bg-[#FFDAD7] p-5 flex items-center gap-4">
            <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-sm">
              <span className="material-symbols-outlined text-[#874F4C] filled-icon">set_meal</span>
            </div>
            <div>
              <p className="font-black text-[#874F4C] text-[15px]">Harbor Grill</p>
              <p className="text-[12px] font-bold text-[#874F4C]/60">Seasonal Catch</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2 className="text-[20px] font-black text-on-surface mb-6">Community Discoveries</h2>
      <article className="tile-card tile-surface p-0 overflow-hidden">
        <div className="p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img className="w-12 h-12 rounded-full border-4 border-[#F2F4F3]" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCxVIK0NqY36ossGVAs-fbu5w1hSsPYHEx-afCxf0c0IHtgXLCZDR20HhGpw1kYpSIxoLPhRsH-lXqWWgQhZaqf1TRWiQtC_pr8GAIzJTkvGuA0dUBrKQWIa_XrB6-k0h5LwBttkX4_aD3it_fEYGvIxJgbCK4hV1JDMlqv8EGxwRsWcXTmGA0ITWSWHx9AM8BhRTq9PL49pSj6bGmg6wtkqSkRJzlk9SarUuSBX0YMeS599-uOJeZDe67jo_Xjp4o0mfBv0Xq92SDm" alt="User" />
            <div>
              <h4 className="font-black text-on-surface text-[15px]">Mushroom_Master</h4>
              <span className="text-[10px] font-bold text-outline uppercase tracking-widest bg-[#E9E8E5] px-2 py-0.5 rounded-full">Elder Forager</span>
            </div>
          </div>
          <span className="material-symbols-outlined text-outline">more_horiz</span>
        </div>
        <div className="px-6 pb-6 relative h-64 overflow-hidden">
          <img className="w-full h-full object-cover rounded-[24px]" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCj0gcWllogpZlrbV6XEMg4xzIGfcjAOzYBEZcnPp6OPmaxFvQMr4k-9OCCzZWDN8v3TMcSY0wiApNnmw-zk5idK7do-5is8P-pvX8ZDibijaL8FrUpBa9Yh8cqMlA17wvCeh9DBR1UpnU3UE5puQpwyajb6fgxLer3sUjsW_rN0doUHRZPHlRUs3hl0NKHKCX_dBvluLd7yI6AwUvfDc8NObWLpUojb2sLFj3l1A8FbM-RhAQLlniV54iD7jtdPdxXR6f-7k8iRuF2" alt="Post" />
          <div className="absolute top-4 right-10 bg-[#194F42]/80 backdrop-blur-md text-white px-4 py-1.5 rounded-full flex items-center gap-2 text-[11px] font-black border-b-2 border-black/20">
            <span className="material-symbols-outlined text-[14px] filled-icon text-[#B7EEDB]">auto_awesome</span> LEGENDARY FIND
          </div>
        </div>
      </article>
    </section>
  </main>
);

const AlarmModal = ({ onClose }) => (
  <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-6 animate-in fade-in duration-300">
    <div className="bg-white w-full max-w-sm rounded-[40px] border-b-[10px] border-[#E7C269] overflow-hidden shadow-2xl animate-in zoom-in-95 duration-300">
      <div className="bg-[#FFDF96] p-8 flex flex-col items-center text-center gap-3">
        <div className="px-6 py-1.5 bg-white/90 rounded-full border-2 border-[#E7C269] mb-2 shadow-sm">
          <span className="text-[12px] font-black text-[#765B06] uppercase tracking-[0.2em]">Lucky Chance!</span>
        </div>
        <h2 className="text-[20px] font-black text-[#765B06] leading-tight">Specialty Alert: Fresh Strawberries within 50m!</h2>
      </div>
      <div className="p-8 space-y-6">
        <div className="relative aspect-video rounded-[24px] overflow-hidden border-4 border-[#F2F4F3] shadow-inner">
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBGU8k3dNoNXQXhuPyg_Ykfr4o9n0iJUBFvyjLON27REw7h7O44DAGDIXWCWoS5icMTRzKjC5fNRbTWx6MqwH6-AikhlcCtSiMsNSb1EmS39Z0assp0hAD3qUH2D27uL6OOeEmFIGhcls6jjdLPesVF5bYcdTgZzaRuJaId3I5YCt-qqXutrhXMKEUPZTrzXa6tsl8IkpxlIRh-Swy5pVId3ylMKEy1PXE1xzoTSkksDYi8YjJMnTwp-bv7Wqj-CfZKn9H6Z0zg9n_n" className="w-full h-full object-cover" alt="Store Hint" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent flex items-end p-4">
            <p className="text-white text-[12px] font-bold flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">image</span> Store Hint Photo
            </p>
          </div>
        </div>
        
        {/* Character & Bubble exactly as image */}
        <div className="flex items-end gap-3 w-full">
          <div className="w-20 h-20 shrink-0">
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCAZaxSgYSUEsgX5qzmU9b3flhYyW4QgXwOYxB2F4IQLgkjpgToGPIw9lIU17pCJzOZ6ORhPql89zN-MUWozO4QAU5FfnkkA_mZCTkdGhGTfjIS7V2UiQHlzruAKJsO6fb8s9FB3pgyRJyporcN4qdEPnBPtZ6UNFwyFWhgst9VgQoVH_XZDFuyMe-xuFa6JRc0X16R2bdKfxFO08RBEGwlIpoNkI3DmxfLbTJcRRsbGZvJoJLWETsOjXVD-lwLD6OKXIP7bjrFyOde" className="w-full h-full object-contain" alt="Guide" />
          </div>
          <div className="flex-1 bg-[#F2F4F3] p-4 rounded-[20px] rounded-bl-none border-2 border-white shadow-sm relative">
            <p className="text-[13px] font-bold text-on-surface-variant italic leading-relaxed">"Look! That stall with the red striped awning just around the corner has the best harvest today!"</p>
          </div>
        </div>

        <div className="flex gap-4">
          <button onClick={onClose} className="flex-1 bg-white border-b-4 border-[#DBDAD7] text-on-surface font-black py-4 rounded-[20px] flex items-center justify-center gap-2 active:translate-y-1 active:border-b-0 transition-all text-[14px]">
            <span className="material-symbols-outlined text-[20px]">visibility</span> Check Hint
          </button>
          <button className="flex-1 bg-[#FFDF96] border-b-4 border-[#E7C269] text-[#765B06] font-black py-4 rounded-[20px] flex items-center justify-center gap-2 active:translate-y-1 active:border-b-0 transition-all text-[14px]">
            <span className="material-symbols-outlined text-[20px] filled-icon">near_me</span> Directions
          </button>
        </div>
      </div>
    </div>
  </div>
);

// --- Main App ---

export default function App() {
  const [currentView, setView] = useState('home');
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowAlert(true), 2500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="min-h-screen bg-[#F2F4F3] selection:bg-[#B7EEDB] overflow-x-hidden">
      <TopAppBar />
      
      {currentView === 'home' && <HomeView />}
      {currentView === 'collection' && <CollectionView />}
      {currentView === 'community' && <CommunityView />}
      {currentView === 'camera' && (
        <main className="pt-40 flex items-center justify-center min-h-[60vh] px-6 animate-in fade-in duration-500">
          <div className="text-center p-12 bg-white rounded-[40px] border-b-8 border-[#F2F4F3] max-w-sm w-full">
            <div className="w-24 h-24 bg-[#B7EEDB] rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
              <span className="material-symbols-outlined text-[#346859] text-[56px]">photo_camera</span>
            </div>
            <h2 className="text-[24px] font-black mb-2">Camera Mode</h2>
            <p className="text-outline text-[14px] font-bold">Capture seasonal ingredients to complete your collection!</p>
          </div>
        </main>
      )}

      {showAlert && <AlarmModal onClose={() => setShowAlert(false)} />}

      <BottomNavBar activeView={currentView} setView={setView} />
    </div>
  );
}
