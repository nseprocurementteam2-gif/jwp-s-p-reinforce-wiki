import React, { useState, useEffect } from 'react';

// --- Shared Components ---

const TopAppBar = ({ level = 12 }) => (
  <header className="fixed top-0 w-full z-50 bg-[#B4EBD8] border-b-4 border-emerald-200/50 shadow-[0_4px_0_0_rgba(180,235,216,0.5)]">
    <div className="flex justify-between items-center w-full px-6 py-4 max-w-screen-xl mx-auto">
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-10 rounded-full border-4 border-white bg-white overflow-hidden shadow-sm">
          <img 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKPScLHnYOazqSCRMT0_JGDB-fGp7x94yFZEypVc04Pz52huUruQVRG9irLaUvajeXMxI_yQhuQ_bMpknGAXZmg1nS3E133_jrIWskW1KKJjwjy4-RBYNDRwbGgUk-YD88Sn9Y7wLPcWpZ6y1NFZMWwZUO0nnsEJNRWOvwEyt42JGiEJGf9XFTmaBnMjtEWoGHoCf79EyLmdG08RaL9Ae31MHDDmPy462fIqO7aRrhHX-oJJXvfoHOM5aXkiWdMcEa3LOnkgwctWbG" 
            alt="Avatar" 
            className="w-full h-full object-cover"
          />
        </div>
        <div>
          <h1 className="text-lg font-black text-emerald-950 leading-tight">Novice Gourmet</h1>
          <p className="text-[10px] font-bold text-emerald-800/70 uppercase tracking-widest">Spring Season</p>
        </div>
      </div>
      <div className="flex items-center gap-2 px-3 py-1 bg-white/40 rounded-full border-2 border-white/60">
        <span className="material-symbols-outlined text-emerald-900 text-sm filled-icon">military_tech</span>
        <span className="font-bold text-emerald-900 text-xs">Level {level}</span>
      </div>
    </div>
    <div className="bg-secondary text-on-secondary py-1 overflow-hidden border-b-2 border-secondary-fixed/30">
      <div className="max-w-screen-xl mx-auto flex items-center px-6">
        <div className="flex items-center gap-2 bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tighter mr-4 z-10 shrink-0">
          <span className="material-symbols-outlined text-xs">campaign</span> LIVE
        </div>
        <div className="relative flex-1 overflow-hidden h-5">
          <div className="ticker-scroll text-[11px] font-bold flex gap-12 items-center">
            <span>Gyeongju: Fresh spring strawberries spotted at the central market! 🍓</span>
            <span>Jeju: Hallabong season is at its peak! 🍊</span>
            <span>Hadong: First flush green tea leaves are ready for harvest! 🍃</span>
            <span>Yangpyeong: Wild chives are abundant near the riverside! 🌱</span>
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
    <nav className="fixed bottom-0 left-0 w-full z-50 bg-white border-t-4 border-emerald-50 rounded-t-[24px] shadow-[0_-4px_12px_rgba(0,0,0,0.05)]">
      <div className="flex justify-around items-end w-full px-4 pb-6 pt-2 max-w-screen-xl mx-auto">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setView(item.id)}
            className={`flex flex-col items-center justify-center px-5 py-2 transition-all active:scale-95 duration-150 ${
              activeView === item.id 
                ? 'bg-emerald-100 text-emerald-900 rounded-[16px] translate-y-[-4px] border-b-4 border-emerald-300' 
                : 'text-slate-400 hover:bg-emerald-50'
            }`}
          >
            <span className={`material-symbols-outlined ${activeView === item.id ? 'filled-icon' : ''}`}>
              {item.icon}
            </span>
            <span className="text-[10px] font-bold uppercase tracking-wider mt-1">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};

// --- Views ---

const HomeView = () => (
  <main className="pb-32 px-6 max-w-screen-xl mx-auto pt-40 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <section className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div className="lg:col-span-8 bg-primary-container p-6 rounded-[32px] shadow-[0_4px_0_0_#9bd2bf] flex flex-col justify-between">
        <div>
          <h2 className="text-2xl font-black text-on-primary-container mb-2">Adventure Progress</h2>
          <p className="text-sm text-on-primary-container opacity-80 mb-6">You're 240 XP away from becoming a <span className="font-bold underline">Seasonal Sous-Chef</span>!</p>
        </div>
        <div className="relative pt-4">
          <div className="flex justify-between mb-2">
            <span className="text-xs font-bold text-on-primary-container">Level 12</span>
            <span className="text-xs font-bold text-on-primary-container">Level 13</span>
          </div>
          <div className="h-6 w-full bg-white/40 rounded-full overflow-hidden p-1">
            <div className="h-full bg-primary rounded-full relative" style={{ width: '75%' }}>
              <div className="absolute right-0 top-0 h-full w-4 bg-white/20 skew-x-12"></div>
            </div>
          </div>
          <div className="absolute top-8 left-[25%] -translate-x-1/2">
            <span className="material-symbols-outlined text-secondary text-lg">energy_savings_leaf</span>
          </div>
          <div className="absolute top-8 left-[50%] -translate-x-1/2">
            <span className="material-symbols-outlined text-secondary text-lg filled-icon">local_florist</span>
          </div>
          <div className="absolute top-8 left-[75%] -translate-x-1/2">
            <span className="material-symbols-outlined text-secondary text-lg">grade</span>
          </div>
        </div>
      </div>
      <div className="lg:col-span-4 bg-secondary-container p-6 rounded-[32px] shadow-[0_4px_0_0_#e7c269] flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 bg-white/50 rounded-full flex items-center justify-center mb-4 border-4 border-white">
          <span className="material-symbols-outlined text-secondary text-3xl filled-icon">restaurant</span>
        </div>
        <h3 className="text-xl font-bold text-on-secondary-container">14 Recipes</h3>
        <p className="text-xs font-bold text-on-secondary-container opacity-70">Mastered this Season</p>
        <button className="mt-4 px-6 py-2 bg-white rounded-2xl font-bold text-secondary shadow-[0_4px_0_0_#efeeeb] press-effect">
          View Log
        </button>
      </div>
    </section>

    <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div className="bg-surface-container rounded-[32px] p-6 shadow-[0_4px_0_0_#dbdad7]">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold">Daily Quests</h3>
          <span className="bg-error-container text-on-error-container text-[10px] font-bold px-2 py-1 rounded-lg">2h Left</span>
        </div>
        <div className="space-y-4">
          {[
            { title: 'Catch the Spring Strawberry', desc: 'Find local farm varieties', icon: 'shopping_basket', bg: 'bg-primary-container', color: 'text-primary', done: false },
            { title: 'Taste the Spring Sea Bream', desc: 'Identify Sakura Tai texture', icon: 'set_meal', bg: 'bg-tertiary-container', color: 'text-tertiary', done: true },
          ].map((quest, i) => (
            <div key={i} className="flex items-center gap-4 bg-white p-4 rounded-2xl border-b-4 border-surface-dim press-effect">
              <div className={`w-12 h-12 ${quest.bg} rounded-xl flex items-center justify-center`}>
                <span className={`material-symbols-outlined ${quest.color}`}>{quest.icon}</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-bold">{quest.title}</p>
                <p className="text-[10px] text-outline italic">{quest.desc}</p>
              </div>
              <span className={`material-symbols-outlined ${quest.done ? 'text-primary filled-icon' : 'text-outline-variant'}`}>
                {quest.done ? 'check_circle' : 'radio_button_unchecked'}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="lg:col-span-2 bg-white rounded-[32px] overflow-hidden shadow-sm border-b-4 border-surface-container flex flex-col md:flex-row">
        <div className="md:w-1/2 relative min-h-[200px]">
          <img 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDLWtLtVDoXBKMoQUty8yVad4evHcThUeCxMktBt9xm5u5UtsTsDKtuj6Xm4KvRo5kuHJ9yHFgJMr0zSChEbpdoi849SIBuxQ7RBDWkxDxYpwA3Nn4eNwUWCQxK0xZ3177XFqQADqf1czu617egKFsBgLZmvQNXBVcXsRtaKYSBqam2578vm1HILbQBlxrhZ7tMQbOztmSf3J2r4YH-i4HiKu8T7YCSYVesmD8V7K-UXT2gvJspVLQUKyV7dz-ujNCgDltY5vP23wqX" 
            className="w-full h-full object-cover"
            alt="Spotlight"
          />
          <div className="absolute top-4 left-4 bg-primary text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg">Tonight's Spotlight</div>
        </div>
        <div className="md:w-1/2 p-6 flex flex-col justify-center">
          <div className="flex items-center gap-2 mb-2 text-secondary">
            <span className="material-symbols-outlined text-sm filled-icon">stars</span>
            <span className="text-[10px] font-bold uppercase">Rare Specialty</span>
          </div>
          <h3 className="text-xl font-bold mb-3 leading-tight">Sakura-Smoked Sea Bream</h3>
          <p className="text-xs text-on-surface-variant mb-6 leading-relaxed">
            A delicate harmony of early spring flavors. Cherry wood smoke meets buttery sea bream.
          </p>
          <div className="flex gap-3">
            <button className="flex-1 bg-primary text-on-primary font-bold py-3 rounded-xl shadow-[0_4px_0_0_#194f42] press-effect flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-sm">menu_book</span> Cook
            </button>
            <button className="w-12 h-12 border-2 border-surface-container rounded-xl flex items-center justify-center text-outline press-effect">
              <span className="material-symbols-outlined">bookmark</span>
            </button>
          </div>
        </div>
      </div>
    </section>
  </main>
);

const CollectionView = () => (
  <main className="max-w-screen-xl mx-auto pt-40 px-6 pb-32 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <section>
      <h2 className="text-xl font-black text-primary mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined filled-icon">stars</span> Mastery Badges
      </h2>
      <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
        {[
          { title: 'Strawberry Master', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA0o-9zOu7TzKCAz2WOfZyq_X83Ew3krQ58R_5O8N7A78xS5ygZu64LJXnHivw-E1L3eCXRi9XzBHBy2u7jhq0RP8ZnyjFmKmP98W0emoBhgoW8hwRNfO_VPkNmxvXH5jLu59y9260O3VK48dnfKFNhqtTNLHlK8uIexbPRNO7RrFGMIs3n8UmcQyD87oH4zO9FPSoavqmGHeUVCNPkicIDzaNjaACVwiUlA75FZfis97NAZ_28-nwRDfx_T_ZstNTaT62QHg7JGlaV', bg: 'bg-secondary-container', border: 'border-secondary' },
          { title: 'Spring Messenger', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC_ssRJnBO7Pl-roCrGzjz_U9f2Sw2JjdLrHGKcWue78A-QJgKy3oZsSaAosCRIFWCEbr8yDDfzeK6kAitXPhq7f-QtGJSQiP8NUsP0IPYUduuPObTE7mSGTuozc-HG8mH8hrBFPIHL_LI7l0haqWAu3jVjMDxlrrGSFOy_jZ84FnPfEGcL7G0uzBP6LOiuhNDU2pPGaI-Za7ttVu9OGmmnMWcyRz5r4OMlE34BAHsvSWByCkzbzHxfZJs84VY9giGI7dhi06WDQ99t', bg: 'bg-primary-container', border: 'border-primary' },
        ].map((badge, i) => (
          <div key={i} className={`flex-shrink-0 flex flex-col items-center ${badge.bg} p-4 rounded-3xl border-b-4 ${badge.border} shadow-sm`}>
            <img src={badge.img} className="w-16 h-16 mb-2" alt={badge.title} />
            <span className="text-[11px] font-bold text-center">{badge.title}</span>
          </div>
        ))}
      </div>
    </section>

    <nav className="flex gap-2 bg-surface-container-low p-1.5 rounded-2xl overflow-x-auto no-scrollbar">
      {['Fruits', 'Seafood', 'Vegetables', 'Specialties'].map((cat, i) => (
        <button key={i} className={`px-6 py-2 rounded-xl font-bold text-sm whitespace-nowrap transition-all ${i === 0 ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:bg-surface-container-high'}`}>
          {cat}
        </button>
      ))}
    </nav>

    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {[
        { name: 'Shine Muscat', date: 'Oct 12', rarity: 'Rare', bg: 'bg-tertiary-container/30', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDN4zN3rXq7pfRKCuIpWFIswRK2s72kWMydAJz7fjQID13-kG1iPsXx-bkoxHWtLy0LfWIVqv_zMgob0GqpkgSXuqPIndQnqqAJGokyDvLYwiCnrYgf9s9YkrSYtmEltlYFpNQrPudRvl48utRp3FGfuS7KU_nfpzs4WM_cSMh87A_xsCcYuBe5Yy_QXyeHkNxHavxOrHTbqPTItCpXd-VGKybvVZ7nPFizwIp17wW0aGoQly14RLDu4fIdiH8lLiljDubuyz9b7d18' },
        { name: 'King Crab', date: 'Nov 05', rarity: 'Seasonal', bg: 'bg-primary-container/20', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDzP_VxTURJ602Rxro7YqkszBh3SM3IB3713aOI5YS-l7O3Yscjm811V2ZAlMPfTEMSdQWZ02b56jMq3DTu9H_tj3xHZOnhC1LJZv0-6FI6CtfGM71gJM79y-45cGc0EITIGCPGxLd_XLpfb-0HhG9AasXUilLWcei4DNHIGVEjQEPq9AlEaBdPeqcTd8WOXItkQKhF0y_POFcrgPSxbqymF9FfalqdSlTRPmFJazHF2cOZGP8DEmFNu9xIrG9XtDgTlPYJMwAwbmzU' },
        { name: 'Premium Sake', date: 'Sep 28', rarity: 'Common', bg: 'bg-tertiary-container/30', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD4wJ9ALkXLDOelldZu866YrAGHwQrUXiXPh2zcFR1kcjXslwRXa5X8m5Cqqau26OdKjwBmcSN-1ODlj3b1CbdACvxo7oxV100EFnP3y0wVN_89Ph3VlrHdrPLTrPLJqjiX36DCyyuTSr6UlvDYmGWMr35YlZ4blfPEh9y_laXdjR74V5ADRHNdMB6ma_hCVMLOM-NR_q67HVmxj0F2GqYFsn7BU4vl1dZwo3s35RK2SbkHRziQGhMnDs7OvYft56QYmYym2mwqgdPw' },
        { name: 'Napa Cabbage', date: 'Nov 12', rarity: 'Seasonal', bg: 'bg-primary-container/20', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC5aRYAijawWpGSobBitOV5UxBVotJiDMhCbhMlH3qe7uE3OYK2M-TvlU-nUpmJ37UoU2ing8fEwuMhhAhqTvILC60NivE7xx6aV5rwseObJq0RRYkl-sAlXFyD-_uOoQ_rBp7wnZmMblLedwFy5_4c6IM9TJB91muRQCuLX-3SPxnJKq6UFBwplPTWBmsVYyMj14NIPHJ9wbOLp7Kp9dkEuToBcV7LjMX10RrhwfaOAfB0i7XbATDtzVY8TmPXHQNCcgY6O6L0y1xC' },
      ].map((item, i) => (
        <article key={i} className="bg-white rounded-[24px] border-b-4 border-primary-container overflow-hidden group press-effect">
          <div className={`relative aspect-square p-4 ${item.bg}`}>
            <img src={item.img} className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-300" alt={item.name} />
            <div className="absolute top-2 right-2 bg-secondary rounded-full p-1 shadow-sm">
              <span className="material-symbols-outlined text-white text-[10px] filled-icon">verified</span>
            </div>
          </div>
          <div className="p-4">
            <div className="flex justify-between items-start mb-1">
              <h3 className="font-bold text-sm">{item.name}</h3>
              <span className="text-[8px] font-black uppercase bg-secondary-container px-1.5 py-0.5 rounded">{item.rarity}</span>
            </div>
            <p className="text-[10px] font-bold text-outline uppercase mt-1">Collected: {item.date}</p>
          </div>
        </article>
      ))}
    </div>
  </main>
);

const CommunityView = () => (
  <main className="pt-40 px-6 pb-32 max-w-screen-xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <section>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-black">Hot Places</h2>
        <span className="text-xs font-bold text-primary uppercase">View Map</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 bg-surface-container rounded-[24px] p-6 border-b-4 border-surface-dim relative overflow-hidden h-[200px] group cursor-pointer">
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDvAq2d822F_igIZ2blejVWY3Y3_EJ5_zQl-wAc3e25wbCKwNrqhlJCAUGTalKXWB5dXKbuDdthuRdnfWl50op3NJT62h8Lme4s8KInJC_T951gVP3jZ_1ybjL1Hukj_NgwXUshepGvs7KnmQ5ldG-p8REOJ6Cdlrc353tuIAClx7gShxpGE-z0sXwtaRyQLQmxhO-whq6xGHrREj9mkGQxB1LMCEvvjjnDm2X7BCVXkhF6C-9kUuwHYKaEr0OBFkB8tspkGVK3xBdS" className="absolute inset-0 w-full h-full object-cover opacity-50 group-hover:scale-105 transition-all" alt="Map" />
          <div className="relative z-10 h-full flex flex-col justify-end">
            <div className="bg-white/90 backdrop-blur-md p-3 rounded-xl border-b-2 border-emerald-100 w-fit">
              <h3 className="font-bold text-emerald-900">Autumnal Orchards</h3>
              <p className="text-[10px] text-primary flex items-center gap-1">
                <span className="material-symbols-outlined text-xs">location_on</span> Kyoto, Japan
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-4">
          <div className="bg-secondary-container rounded-[24px] p-4 border-b-4 border-secondary-fixed-dim flex items-center gap-3 press-effect">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center"><span className="material-symbols-outlined text-secondary">bakery_dining</span></div>
            <div><p className="font-bold text-xs">Sugar Bloom</p><p className="text-[10px] opacity-70">Rare Pastries</p></div>
          </div>
          <div className="bg-tertiary-container rounded-[24px] p-4 border-b-4 border-tertiary-fixed-dim flex items-center gap-3 press-effect">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center"><span className="material-symbols-outlined text-tertiary">set_meal</span></div>
            <div><p className="font-bold text-xs">Harbor Grill</p><p className="text-[10px] opacity-70">Seasonal Catch</p></div>
          </div>
        </div>
      </div>
    </section>

    <section className="space-y-6">
      <h2 className="text-xl font-black">Community Discoveries</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[
          { user: 'Mushroom_Master', rank: 'Elder Forager', text: 'Finally found the elusive Golden Cap! 🍄✨', location: 'Whispering Woods', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCj0gcWllogpZlrbV6XEMg4xzIGfcjAOzYBEZcnPp6OPmaxFvQMr4k-9OCCzZWDN8v3TMcSY0wiApNnmw-zk5idK7do-5is8P-pvX8ZDibijaL8FrUpBa9Yh8cqMlA17wvCeh9DBR1UpnU3UE5puQpwyajb6fgxLer3sUjsW_rN0doUHRZPHlRUs3hl0NKHKCX_dBvluLd7yI6AwUvfDc8NObWLpUojb2sLFj3l1A8FbM-RhAQLlniV54iD7jtdPdxXR6f-7k8iRuF2', avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCxVIK0NqY36ossGVAs-fbu5w1hSsPYHEx-afCxf0c0IHtgXLCZDR20HhGpw1kYpSIxoLPhRsH-lXqWWgQhZaqf1TRWiQtC_pr8GAIzJTkvGuA0dUBrKQWIa_XrB6-k0h5LwBttkX4_aD3it_fEYGvIxJgbCK4hV1JDMlqv8EGxwRsWcXTmGA0ITWSWHx9AM8BhRTq9PL49pSj6bGmg6wtkqSkRJzlk9SarUuSBX0YMeS599-uOJeZDe67jo_Xjp4o0mfBv0Xq92SDm' },
          { user: 'Baker_Ben', rank: 'Pie Specialist', text: 'The Honeycrisps are finally ripe! Made this tart. 🍎🥧', location: 'Sunny Orchard', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAJsWBmi9IWWVm3EokJBL1viqoE22VJNaH3DOW766VfOaN1LlI1Bo7JKE1hLfX1imJTWMDcx7pARBF1IxSnbguZCSe4C-EZxoTI3pgXVMYIkwHQsNhEjG0rU6ZpUwliuHHEPomzdICuxs0V1uBHFJtDsJ46wIk-aXfy0z3oSzoZ56ov11zRXo8S9alUT6mOtbG1qExNBqjHud15ReRsAYIi4N2JkJB7k4yMtVoPpw6QsPxEfUhugyjiMdwg4dnwZtWUPuAsu176yPvI', avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCwIhwMiIjD8mg6Kc8PeG5xHwRt0B_D7MoOQBjtCe-wCwwdGKhMIfNzCnZYUBzx2MyUyji3N_2bfCBP4YtTrOB8sUpNY5nfkjYO32XrWbVI_rLZUJyhyg9KwYdIhDjRDrBi7XtXkNX2UtK8Bbw7WB52t9Mklql4ELujI3oabxm9PYysjdSyXlrsEyNOpeDLH_VhtKDxgvvhzyZ0CwpSvvXp2m5GbKngSLGeWiE-TgQkKqYsasxxAlie1BummvEOJHn530t7jMypm8ve' },
        ].map((post, i) => (
          <article key={i} className="cottage-card overflow-hidden">
            <div className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <img src={post.avatar} className="w-10 h-10 rounded-full border-2 border-emerald-100" alt="Avatar" />
                <div><p className="font-bold text-sm">{post.user}</p><p className="text-[10px] text-outline">{post.rank}</p></div>
              </div>
              <span className="material-symbols-outlined text-outline">more_horiz</span>
            </div>
            <div className="mx-4 h-56 rounded-[24px] overflow-hidden relative">
              <img src={post.img} className="w-full h-full object-cover" alt="Post" />
            </div>
            <div className="p-4 space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-primary font-bold text-xs flex items-center gap-1"><span className="material-symbols-outlined text-sm">location_on</span> {post.location}</p>
                <div className="flex gap-2">
                  <button className="flex items-center gap-1 bg-tertiary-container px-3 py-1.5 rounded-full border-b-2 border-tertiary-fixed-dim press-effect">
                    <span className="material-symbols-outlined text-tertiary text-xs filled-icon">favorite</span>
                  </button>
                  <button className="bg-surface-container px-3 py-1.5 rounded-full border-b-2 border-outline-variant press-effect">
                    <span className="material-symbols-outlined text-outline text-xs">chat_bubble</span>
                  </button>
                </div>
              </div>
              <p className="text-xs text-on-surface-variant leading-relaxed">{post.text}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  </main>
);

const AlarmModal = ({ onClose }) => (
  <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-6 animate-in fade-in duration-300">
    <div className="bg-white w-full max-w-md rounded-[40px] border-b-[8px] border-secondary overflow-hidden shadow-2xl animate-in zoom-in-95 duration-300">
      <div className="bg-secondary-fixed p-6 flex flex-col items-center text-center gap-2 border-b-4 border-secondary-fixed-dim">
        <div className="px-4 py-1 bg-white/90 rounded-full border-2 border-secondary mb-2 animate-pulse">
          <span className="text-[10px] font-black text-secondary uppercase tracking-widest">Lucky Chance!</span>
        </div>
        <h2 className="text-xl font-black text-on-secondary-fixed leading-tight">Fresh Strawberries within 50m!</h2>
      </div>
      <div className="p-8 flex flex-col gap-6 items-center">
        <div className="relative w-full aspect-video rounded-3xl overflow-hidden border-4 border-surface-container-high bg-surface-container shadow-inner">
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBGU8k3dNoNXQXhuPyg_Ykfr4o9n0iJUBFvyjLON27REw7h7O44DAGDIXWCWoS5icMTRzKjC5fNRbTWx6MqwH6-AikhlcCtSiMsNSb1EmS39Z0assp0hAD3qUH2D27uL6OOeEmFIGhcls6jjdLPesVF5bYcdTgZzaRuJaId3I5YCt-qqXutrhXMKEUPZTrzXa6tsl8IkpxlIRh-Swy5pVId3ylMKEy1PXE1xzoTSkksDYi8YjJMnTwp-bv7Wqj-CfZKn9H6Z0zg9n_n" className="w-full h-full object-cover" alt="Hint" />
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
            <p className="text-white text-[10px] font-bold flex items-center gap-2"><span className="material-symbols-outlined text-sm">image</span> Store Hint Photo</p>
          </div>
        </div>
        <div className="flex items-center gap-4 w-full">
          <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCAZaxSgYSUEsgX5qzmU9b3flhYyW4QgXwOYxB2F4IQLgkjpgToGPIw9lIU17pCJzOZ6ORhPql89zN-MUWozO4QAU5FfnkkA_mZCTkdGhGTfjIS7V2UiQHlzruAKJsO6fb8s9FB3pgyRJyporcN4qdEPnBPtZ6UNFwyFWhgst9VgQoVH_XZDFuyMe-xuFa6JRc0X16R2bdKfxFO08RBEGwlIpoNkI3DmxfLbTJcRRsbGZvJoJLWETsOjXVD-lwLD6OKXIP7bjrFyOde" className="w-20 h-20 object-contain" alt="Guide" />
          <div className="flex-1 bg-surface-container-low p-4 rounded-2xl border-2 border-dashed border-outline-variant relative">
            <div className="absolute -left-2 top-1/2 -translate-y-1/2 w-4 h-4 bg-surface-container-low rotate-45 border-l-2 border-b-2 border-dashed border-outline-variant"></div>
            <p className="text-[11px] font-bold text-on-surface-variant italic">"Look! That stall with the red striped awning has the best harvest today!"</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 w-full">
          <button onClick={onClose} className="bg-white border-2 border-outline-variant text-on-surface font-bold py-4 rounded-2xl press-effect shadow-[0_4px_0_0_#c0c9c4] text-sm">Dismiss</button>
          <button className="bg-secondary-container border-2 border-secondary text-on-secondary-container font-bold py-4 rounded-2xl press-effect shadow-[0_4px_0_0_#785d09] text-sm">Go Now</button>
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
    // Trigger lucky alert after 3 seconds for demo
    const timer = setTimeout(() => setShowAlert(true), 3000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="min-h-screen bg-background selection:bg-primary-container">
      <TopAppBar />
      
      {currentView === 'home' && <HomeView />}
      {currentView === 'collection' && <CollectionView />}
      {currentView === 'community' && <CommunityView />}
      {currentView === 'camera' && (
        <main className="pt-40 flex items-center justify-center min-h-[60vh]">
          <div className="text-center p-12 bg-white rounded-[40px] shadow-sm border-b-4 border-surface-container">
            <div className="w-24 h-24 bg-primary-container rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="material-symbols-outlined text-primary text-5xl">photo_camera</span>
            </div>
            <h2 className="text-2xl font-black mb-2">Camera Mode</h2>
            <p className="text-on-surface-variant text-sm">Capture seasonal ingredients to complete your collection!</p>
          </div>
        </main>
      )}

      {showAlert && <AlarmModal onClose={() => setShowAlert(false)} />}

      <button className="fixed bottom-32 right-8 w-16 h-16 bg-primary text-on-primary rounded-full shadow-[0_8px_20px_rgba(52,104,89,0.3)] flex items-center justify-center z-40 hover:scale-110 active:scale-95 transition-all border-4 border-primary-container press-effect">
        <span className="material-symbols-outlined text-3xl filled-icon">photo_camera</span>
      </button>

      <BottomNavBar activeView={currentView} setView={setView} />
    </div>
  );
}
