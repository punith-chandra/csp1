import React, { useState, useEffect, useRef } from 'react';
import { 
  Plus, Search, PanelLeftClose, PanelLeft, RotateCcw, 
  Mic, MicOff, Copy, Check, Volume2, VolumeX, ThumbsUp, 
  ThumbsDown, ShieldCheck, BarChart3, BookOpen, 
  Users, Sparkles, ExternalLink, ShieldAlert, FileText, ArrowRight, Languages
} from 'lucide-react';
import { analyzeFoodItem, getFoodItems, sendChatMessage } from '../services/api';
import { t } from '../i18n';

const NUTRIENT_EXPLANATIONS = {
  energy: 'Energy (calories) is the fuel food provides your body.',
  protein: 'Protein helps your body build and repair muscles and other tissues.',
  totalFat: 'Fat provides energy and helps your body absorb some vitamins.',
  carbohydrates: 'Carbohydrates are one of the body’s main sources of energy.',
  fiber: 'Fiber supports digestion.',
  totalSugars: 'Total sugars are included within carbohydrates. The record may not distinguish naturally occurring from added sugar.',
  sodium: 'Sodium is a mineral found in salt. High sodium intake can be a concern for some people.'
};

function getFoodReferenceLinks(foodName) {
  const query = encodeURIComponent(foodName || 'food');
  return [
    { name: 'Google', url: `https://www.google.com/search?q=${query}` },
    { name: 'Bing', url: `https://www.bing.com/search?q=${query}` },
    { name: 'Wikipedia', url: `https://en.wikipedia.org/w/index.php?search=${query}` },
    { name: 'Open Food Facts', url: `https://world.openfoodfacts.org/cgi/search.pl?search_terms=${query}` },
    { name: 'USDA FoodData Central', url: `https://fdc.nal.usda.gov/food-search/?query=${query}` }
  ];
}

function getFoodSubject(text) {
  const match = text.match(/\b(?:about|for|of|on)\s+([a-z][a-z\s-]*?)(?:[?.!]|$)/i);
  return match ? match[1].trim().replace(/\s+(please|thanks)$/i, '') : '';
}

function createFoodContext(foodData) {
  return JSON.stringify({
    foodName: foodData.foodName,
    category: foodData.category,
    overview: foodData.webInformation?.summary,
    product: foodData.productInfo
      ? {
          brand: foodData.productInfo.brand,
          ingredients: foodData.productInfo.ingredients,
          countries: foodData.productInfo.countries
        }
      : undefined,
    nutrition: foodData.nutritionInformation,
    adulterants: foodData.adulterants,
    healthRisks: foodData.healthRisks,
    safeTips: foodData.safeTips,
    storageTips: foodData.storageTips,
    sources: foodData.sources
  });
}

export default function AIChatBoard({ onSwitchToProjectView, onOpenPresentation, initialQuery = '', language = 'en', onLanguageChange }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [foodItems, setFoodItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [speakingId, setSpeakingId] = useState(null);
  const [quickMenuOpen, setQuickMenuOpen] = useState(false);
  const [standardsModalOpen, setStandardsModalOpen] = useState(false);

  // Recent queries list tailored to food safety & purity
  const [chatHistory, setChatHistory] = useState([
    { id: '1', title: 'Milk Adulteration & Purity', query: 'Milk' },
    { id: '2', title: 'Turmeric Metanil Yellow Test', query: 'Turmeric' },
    { id: '3', title: 'Honey Water Purity Test', query: 'Honey' },
    { id: '4', title: 'Edible Oil Argemone Check', query: 'Edible Oil' },
    { id: '5', title: 'Ghee & Vanaspati Detection', query: 'Ghee' },
    { id: '6', title: 'Chilli Powder Brick Dust Check', query: 'Chilli Powder' },
    { id: '7', title: 'Rice Polish & Mineral Oil', query: 'Rice' },
  ]);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  useEffect(() => {
    let isActive = true;

    getFoodItems().then((items) => {
      if (isActive) setFoodItems(Array.isArray(items) ? items : []);
    });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const normalizedInput = inputValue.trim().toLowerCase();
  const foodSuggestions = normalizedInput && !loading
    ? foodItems.filter((item) =>
        [item.foodName, ...(item.aliases || [])].some((name) =>
          name?.toLowerCase().includes(normalizedInput)
        )
      ).slice(0, 6)
    : [];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async (customText = null) => {
    const text = (customText !== null ? customText : inputValue).trim();
    if (!text || loading) return;

    setInputValue('');
    setQuickMenuOpen(false);

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const isInformationQuestion = /\b(more|tell|explain|detail|information|benefit|nutrition|nutrient|calorie|ingredient|health|risk|how|what|why|storage|safe|source)\b/i.test(text);
      if (isInformationQuestion) {
        const subject = getFoodSubject(text);
        const previousFood = [...messages]
          .reverse()
          .find((message) => message.foodData?.isFood)?.foodData;
        let foodContext = previousFood;

        if (subject && (!previousFood || subject.toLowerCase() !== previousFood.foodName.toLowerCase())) {
          const subjectData = await analyzeFoodItem(subject);
          foodContext = subjectData.isFood ? subjectData : null;
        }

        if (foodContext?.isFood) {
          const history = [
            ...messages.filter((message) => message.content).map(({ role, content }) => ({ role, content })),
            { role: 'user', content: text }
          ].slice(-10);
          const response = await sendChatMessage(
            text,
            createFoodContext(foodContext),
            history
          );
          setMessages((prev) => [...prev, {
            id: (Date.now() + 1).toString(),
            role: 'assistant',
            isFoodFollowUp: true,
            foodData: foodContext,
            content: response.reply,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }]);
          setChatHistory((prev) => [
            {
              id: Date.now().toString(),
              title: `${foodContext.foodName} • More information`,
              query: text
            },
            ...prev.filter((item) => item.query.toLowerCase() !== text.toLowerCase())
          ]);
          return;
        }
      }

      const foodData = await analyzeFoodItem(text);

      let assistantMessage;
      if (foodData.isFood) {
        assistantMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          foodData: foodData,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
      } else {
        const isUncertain = foodData.classification === 'uncertain';
        assistantMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          isNonFood: !isUncertain,
          isUncertain,
          foodData: foodData,
          content: isUncertain
            ? `The item "${foodData.foodName || text}" could not be confidently classified.`
            : `**${foodData.foodName || text}** is recognized as a non-food item.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
      }

      setMessages((prev) => [...prev, assistantMessage]);

      // Add to sidebar history if not present
      const exists = chatHistory.some((item) => item.query.toLowerCase() === text.toLowerCase());
      if (!exists) {
        setChatHistory((prev) => [
          {
            id: Date.now().toString(),
            title: foodData.isFood ? `${foodData.foodName} Purity Check` : `${text.slice(0, 20)} (Non-food)`,
            query: text
          },
          ...prev
        ]);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Unable to connect to the backend server. Please verify the service is running at http://localhost:8000.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputValue('');
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (inputRef.current) inputRef.current.focus();
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSpeak = (id, text) => {
    if (!window.speechSynthesis) return;

    if (speakingId === id) {
      window.speechSynthesis.cancel();
      setSpeakingId(null);
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.onend = () => setSpeakingId(null);
    utterance.onerror = () => setSpeakingId(null);
    setSpeakingId(id);
    window.speechSynthesis.speak(utterance);
  };

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice input is not supported in this browser. Please type your query.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'te' ? 'te-IN' : 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event) => {
      const speechText = event.results[0][0].transcript;
      setInputValue(speechText);
      handleSend(speechText);
    };

    recognition.start();
  };

  // Helper to extract clean plain text for copy & speak
  const getFoodSummaryText = (food) => {
    if (!food) return '';
    return `${food.foodName} Food Safety Information:\n` +
      `Possible Adulterants: ${food.adulterants?.join(', ')}\n` +
      `Why Adulteration Occurs: ${food.whyAdulterated}\n` +
      `Awareness Test: ${food.testMethod} - ${food.observation}\n` +
      `Health Risks: ${food.healthRisks?.join('; ')}\n` +
      `Safe Buying Tips: ${food.safeTips?.join('; ')}\n` +
      `Disclaimer: Preliminary awareness check only. Laboratory testing is required for scientific confirmation.`;
  };

  return (
    <div className={`flex h-screen bg-[#f7faf8] text-[#0d0d0d] font-sans antialiased overflow-hidden selection:bg-emerald-100 selection:text-emerald-900 ${language === 'te' ? 'font-telugu' : ''}`}>
      
      {/* 1. Left Sidebar: Unique Project Identity & Tools */}
      <aside 
        className={`bg-[#f9fafb] border-r border-[#e5e7eb] flex flex-col justify-between transition-all duration-300 z-30 ${
          sidebarOpen ? 'w-64 sm:w-[270px]' : 'w-0 -translate-x-full sm:translate-x-0 sm:w-0'
        } overflow-hidden`}
      >
        <div className="p-3 flex flex-col h-full">
          
          {/* Top Title: Unique Project Name */}
          <div className="flex items-center justify-between px-2 py-2 mb-2">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center font-bold shadow-xs">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <div>
                <span className="font-extrabold text-[15px] text-[#0f172a] tracking-tight block leading-tight">
                  FoodPure AI
                </span>
                <span className="text-[10px] font-semibold text-emerald-600 block uppercase tracking-wider">
                  {t(language, 'Food Safety & Purity')}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-1 text-slate-500">
              <button 
                onClick={handleNewChat}
                className="p-1.5 hover:text-slate-900 rounded-lg hover:bg-slate-200 transition-colors"
                title={t(language, 'New analysis')}
              >
                <Plus className="w-4 h-4" />
              </button>
              <button 
                onClick={() => setSidebarOpen(false)}
                className="p-1.5 hover:text-slate-900 rounded-lg hover:bg-slate-200 transition-colors"
                title={t(language, 'Collapse sidebar')}
              >
                <PanelLeftClose className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* "New Analysis" Button */}
          <button
            onClick={handleNewChat}
            className="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-[13px] font-semibold text-emerald-800 transition-colors mb-3 border border-emerald-200/60"
          >
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>{t(language, 'New Food Analysis')}</span>
          </button>

          {/* Project Feature Tools */}
          <div className="space-y-0.5 mb-3 text-[13px] text-slate-600 font-medium">
            <button 
              onClick={handleNewChat}
              className="flex items-center gap-2.5 w-full px-3 py-1.5 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors"
            >
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>{t(language, 'Food Safety Analyzer')}</span>
            </button>
            <button 
              onClick={() => setStandardsModalOpen(true)}
              className="flex items-center gap-2.5 w-full px-3 py-1.5 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors"
            >
              <BookOpen className="w-4 h-4 text-teal-600" />
              <span>{t(language, 'FSSAI & AGMARK Rules')}</span>
            </button>
            <button 
              onClick={onSwitchToProjectView}
              className="flex items-center gap-2.5 w-full px-3 py-1.5 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors"
            >
              <BarChart3 className="w-4 h-4 text-blue-600" />
              <span>{t(language, 'Survey & Community Stats')}</span>
            </button>
            <button 
              onClick={onOpenPresentation}
              className="flex items-center gap-2.5 w-full px-3 py-1.5 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors"
            >
              <Users className="w-4 h-4 text-amber-600" />
              <span>{t(language, 'Project Team & Guide')}</span>
            </button>
            <button 
              onClick={onSwitchToProjectView}
              className="flex items-center gap-2.5 w-full px-3 py-1.5 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition-colors"
            >
              <FileText className="w-4 h-4 text-indigo-600" />
              <span>{t(language, 'Full Website Showcase')}</span>
            </button>
          </div>

          {/* Section: Recent Food Inquiries */}
          <div className="px-3 pt-3 pb-1 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            {t(language, 'Recent Analyses')}
          </div>

          {/* History List */}
          <div className="flex-1 overflow-y-auto space-y-0.5 pr-1 custom-scrollbar">
            {chatHistory.map((item) => (
              <button
                key={item.id}
                onClick={() => handleSend(item.query)}
                className="w-full text-left px-3 py-1.5 rounded-lg text-[13px] text-slate-700 hover:text-emerald-800 hover:bg-emerald-50/70 transition-colors truncate block"
              >
                {item.title}
              </button>
            ))}
          </div>

          {/* Sidebar Bottom: Lead Profile & Sri Vasavi College Info */}
          <div className="pt-2 border-t border-slate-200 mt-auto space-y-2">
            
            {/* User Profile (Puneeth chandra Peethala) */}
            <div 
              onClick={onOpenPresentation}
              className="flex items-center gap-3 px-2 py-1.5 rounded-xl hover:bg-slate-100 transition-colors cursor-pointer"
              title={t(language, 'Click to view Project Team & Guide')}
            >
              <div className="w-8 h-8 rounded-full bg-emerald-700 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-xs">
                PP
              </div>
              <div className="overflow-hidden leading-tight">
                <div className="text-[13px] font-bold text-slate-900 truncate">
                  Puneeth chandra Peethala
                </div>
                <div className="text-[11px] text-emerald-700 font-semibold truncate">
                  {t(language, 'Project Lead')} • 24A81A05G9
                </div>
              </div>
            </div>

            {/* College & Department Badge */}
            <button
              onClick={onOpenPresentation}
              className="w-full py-1.5 px-3 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-[11px] font-semibold flex items-center justify-center gap-1.5 transition-colors border border-slate-200"
              title={t(language, 'Sri Vasavi Engineering College (Autonomous), Department of CSE')}
            >
              <span>🏛️ Sri Vasavi Engg. College (CSE)</span>
            </button>

          </div>

        </div>
      </aside>

      {/* 2. Main Center Content Canvas */}
      <div className="flex-1 flex flex-col h-full bg-[radial-gradient(ellipse_at_top,_#ecfdf5_0%,_#ffffff_42%,_#f8fafc_100%)] relative overflow-hidden">
        
        {/* Top Header Bar */}
        <header className="h-14 flex items-center justify-between px-4 sm:px-6 z-20 border-b border-slate-200/70 bg-white/75 backdrop-blur-xl">
          <div className="flex items-center gap-2">
            {!sidebarOpen && (
              <div className="flex items-center gap-2">
                <button 
                  onClick={() => setSidebarOpen(true)}
                  className="p-1.5 text-slate-600 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition-colors mr-1"
                  title={t(language, 'Open sidebar')}
                >
                  <PanelLeft className="w-5 h-5" />
                </button>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-lg bg-emerald-600 text-white flex items-center justify-center">
                    <ShieldCheck className="w-3.5 h-3.5" />
                  </div>
                  <span className="font-bold text-[15px] text-slate-900 tracking-tight">
                    FoodPure AI
                  </span>
                </div>
              </div>
            )}
            <span className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
              <Sparkles className="w-3 h-3" />
              {t(language, 'AI-Powered Food Safety and Purity Analysis')}
            </span>
          </div>

          {/* Top Right: Project Showcase & Presentation buttons */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => onLanguageChange?.(language === 'en' ? 'te' : 'en')}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-emerald-200 bg-emerald-50 text-xs font-bold text-emerald-800 hover:bg-emerald-100 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
              aria-label={language === 'en' ? 'Switch language to Telugu' : 'Switch language to English'}
              title={language === 'en' ? 'తెలుగులో చూపించు' : 'Show in English'}
            >
              <Languages className="w-3.5 h-3.5" />
              <span>{language === 'en' ? 'తెలుగు' : 'English'}</span>
            </button>
            <button
              onClick={onSwitchToProjectView}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full hover:bg-slate-100 text-xs font-semibold text-slate-700 transition-colors border border-slate-200"
              title={t(language, 'Switch to Full Project Website')}
            >
              <BarChart3 className="w-3.5 h-3.5 text-blue-600" />
              <span className="hidden sm:inline">{t(language, 'Project Showcase')}</span>
            </button>

            <button
              onClick={onOpenPresentation}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-xs font-semibold text-white transition-colors shadow-xs"
              title={t(language, 'Review Project Slides & Team')}
            >
              <span>{t(language, 'Presentation')}</span>
            </button>

            <button
              onClick={handleNewChat}
              className="p-1.5 text-slate-500 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition-colors"
              title={t(language, 'New session')}
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Conversation Stream OR Unique Landing Screen */}
        <main className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 max-w-3xl w-full mx-auto flex flex-col justify-between">
          
          {messages.length === 0 ? (
            /* UNIQUE OFFICIAL LANDING SCREEN */
            <div className="flex-1 flex flex-col items-center justify-center my-auto text-center px-4 py-8 animate-fadeIn">
              
              <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-white/80 px-3 py-1.5 text-[11px] font-bold uppercase tracking-wider text-emerald-800 shadow-sm mb-5">
                <Sparkles className="h-3.5 w-3.5" />
                {t(language, 'Community Service Project')} • Sri Vasavi Engineering College
              </div>

              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-700 via-teal-600 to-cyan-500 text-white flex items-center justify-center shadow-[0_12px_35px_rgba(5,150,105,0.25)] mb-5">
                <ShieldCheck className="w-9 h-9" />
              </div>

              <h1 className="text-[26px] sm:text-[34px] font-black text-slate-900 tracking-tight mb-2 leading-tight max-w-2xl">
                {t(language, 'AI-Powered Food Safety and Purity Analysis')}
              </h1>
              
              <p className="text-slate-600 text-sm sm:text-base max-w-xl mx-auto mb-8 font-medium">
                {t(language, 'Detect adulteration risks, learn simple scientific home tests, and verify consumer food safety standards.')}
              </p>

              {/* Quick food staple chips */}
              <div className="w-full max-w-xl grid grid-cols-2 sm:grid-cols-3 gap-2.5 text-left mb-6">
                {[
                  { name: 'Milk', desc: 'Water, Starch & Urea test', icon: '🥛' },
                  { name: 'Turmeric', desc: 'Metanil Yellow & Chalk check', icon: '🌶️' },
                  { name: 'Honey', desc: 'Water solubility & wick test', icon: '🍯' },
                  { name: 'Edible Oil', desc: 'Argemone oil & nitric acid test', icon: '🛢️' },
                  { name: 'Ghee', desc: 'Vanaspati & Furfural check', icon: '🧈' },
                  { name: 'Chilli Powder', desc: 'Brick powder & Sudan dye', icon: '🌶️' },
                ].map((item) => (
                  <button
                    key={item.name}
                    onClick={() => handleSend(item.name)}
                    className="p-3 rounded-xl border border-slate-200 hover:border-emerald-400 hover:bg-emerald-50/50 transition-all text-left group bg-white shadow-xs"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-lg">{item.icon}</span>
                      <span className="font-bold text-sm text-slate-900 group-hover:text-emerald-700">
                        {t(language, item.name)}
                      </span>
                    </div>
                        <div className="text-[11px] text-slate-500 leading-tight">
                      {t(language, item.desc)}
                    </div>
                  </button>
                ))}
              </div>

              <div className="text-[11px] text-slate-400 font-medium">
                {t(language, 'Department of Computer Science and Engineering • Sri Vasavi Engineering College')}
              </div>

            </div>
          ) : (
            /* Clean Conversational Feed (NO ASCII Diagram) */
            <div className="space-y-6 pb-6">
              {messages.map((msg) => (
                <div key={msg.id} className="space-y-4 animate-fadeIn">
                  
                  {/* User Message Bubble */}
                  {msg.role === 'user' && (
                    <div className="flex justify-end gap-3">
                      <div className="bg-slate-100 text-slate-900 px-4 py-2.5 rounded-2xl rounded-tr-sm max-w-[85%] text-[15px] font-normal leading-relaxed border border-slate-200">
                        {msg.content}
                      </div>
                    </div>
                  )}

                  {/* Assistant Message (Clean natural text - NO ASCII DIAGRAM) */}
                  {msg.role === 'assistant' && (
                    <div className="space-y-4 max-w-full">
                      
                      {/* Non-food Response */}
                      {(msg.isNonFood || msg.isUncertain) && (
                        <div className="text-[15px] text-slate-900 leading-relaxed space-y-3 bg-amber-50/70 p-4 rounded-2xl border border-amber-200">
                          <div className="flex items-center gap-2 text-amber-800 font-bold text-base">
                            <ShieldAlert className="w-5 h-5 text-amber-600" />
                            <span>
                              {t(language, msg.isUncertain ? 'Unable to classify item' : 'Non-Food Item Detected')}: {t(language, msg.foodData?.foodName || '')}
                            </span>
                          </div>
                          <p className="text-slate-700">
                            {msg.isUncertain
                              ? t(language, 'This item is not in the food reference database, so the app cannot safely predict adulterants or provide a product test.')
                              : <>{t(language, 'AI-Powered Food Safety and Purity Analysis')} {t(language, 'is designed specifically for food commodities and edible grocery items.')}</>}
                          </p>
                          <p className="text-slate-600 text-sm">
                            {msg.isUncertain
                              ? t(language, 'Use these web searches to learn more. They open external search pages; this app does not fetch or verify live search results.')
                              : <>{t(language, 'Please check an edible grocery item such as')} <strong>{['Milk', 'Turmeric', 'Chilli Powder', 'Honey', 'Sugar', 'Ghee', 'Edible Oil'].map((food) => t(language, food)).join(', ')}</strong> {t(language, 'to inspect common adulterants and preliminary home checks.')}</>}
                          </p>
                          {msg.foodData?.sources?.length > 0 && (
                            <div className="flex flex-wrap gap-2 pt-1">
                              {msg.foodData.sources.map((source) => (
                                <a
                                  key={source.url}
                                  href={source.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-white text-xs font-semibold text-sky-800 border border-sky-200 hover:bg-sky-50"
                                >
                                  {source.name}<ExternalLink className="w-3 h-3" />
                                </a>
                              ))}
                            </div>
                          )}
                          <div className="flex flex-wrap gap-2 pt-1">
                            {['Milk', 'Turmeric', 'Honey', 'Ghee', 'Edible Oil'].map((food) => (
                              <button
                                key={food}
                                onClick={() => handleSend(food)}
                                className="px-3 py-1 rounded-full bg-white hover:bg-emerald-50 text-xs font-semibold text-emerald-800 border border-emerald-300 transition-colors"
                              >
                                {t(language, 'Check')} {t(language, food)}
                              </button>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Food Safety Conversational Response */}
                      {msg.isFoodFollowUp && (
                        <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 text-[15px] leading-relaxed text-slate-800">
                          <h3 className="mb-2 font-bold text-sky-950">
                            {t(language, 'More about')} {t(language, msg.foodData.foodName)}
                          </h3>
                          <p className="whitespace-pre-line">{msg.content}</p>
                          <div className="mt-3 flex flex-wrap gap-2 border-t border-sky-200 pt-3">
                            {getFoodReferenceLinks(msg.foodData.foodName).map((source) => (
                              <a
                                key={source.name}
                                href={source.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 rounded-lg border border-sky-200 bg-white px-3 py-1.5 text-xs font-semibold text-sky-800 hover:bg-sky-100"
                              >
                                {source.name}<ExternalLink className="h-3 w-3" />
                              </a>
                            ))}
                          </div>
                        </div>
                      )}

                      {msg.foodData?.isFood && !msg.isFoodFollowUp && (
                        <div className="text-[15px] text-slate-900 leading-relaxed space-y-4 font-sans">
                          
                          {/* Heading */}
                          <div className="border-b border-slate-100 pb-2">
                            <div className="flex items-center gap-2">
                              <h2 className="text-xl font-bold text-slate-900">
                                {t(language, msg.foodData.foodName)} – {t(language, 'Safety & Purity Advisory')}
                              </h2>
                              <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                                {t(language, 'Reference guidance')}
                              </span>
                            </div>
                            <p className="text-xs text-slate-500 mt-0.5">
                              {t(language, 'Category:')} {t(language, msg.foodData.category || 'Food Commodity')} • {t(language, 'System: AI-Powered Food Safety and Purity Analysis')}
                            </p>
                          </div>

                          {/* Online food information and plain-language nutrition */}
                          <section className="space-y-3 rounded-xl border border-sky-200 bg-sky-50/70 p-4">
                            <h3 className="font-bold text-sky-950 text-base">
                              {t(language, 'Related food information')}
                            </h3>
                            {msg.foodData.dataSource && (
                              <p className="text-sm text-slate-700">
                                {t(language, 'Online information found from:')} {msg.foodData.dataSource
                                  .replace('Curated food-safety reference with ', '')
                                  .replace(/ data; available fields vary by food$/, '')}.
                              </p>
                            )}
                            {msg.foodData.webInformation && (
                              <div className="rounded-lg bg-white/80 p-3">
                                <h4 className="font-semibold text-slate-800">
                                  {t(language, msg.foodData.webInformation.title)}
                                </h4>
                                <p className="mt-1 text-sm leading-relaxed text-slate-700">
                                  {t(language, msg.foodData.webInformation.summary)}
                                </p>
                              </div>
                            )}
                            {msg.foodData.productInfo && (
                              <div className="space-y-1 text-sm text-slate-700">
                                {msg.foodData.productInfo.brand && <p><strong>{t(language, 'Brand:')}</strong> {msg.foodData.productInfo.brand}</p>}
                                {msg.foodData.productInfo.ingredients && <p><strong>{t(language, 'Listed ingredients:')}</strong> {msg.foodData.productInfo.ingredients}</p>}
                                {msg.foodData.productInfo.countries && <p><strong>{t(language, 'Countries listed:')}</strong> {msg.foodData.productInfo.countries}</p>}
                                {msg.foodData.productInfo.nutritionGrade && <p><strong>{t(language, 'Catalog nutrition grade:')}</strong> {msg.foodData.productInfo.nutritionGrade}</p>}
                              </div>
                            )}
                            {msg.foodData.nutritionInformation && (
                              <div className="rounded-lg bg-white/80 p-3">
                                <h4 className="font-semibold text-slate-800">
                                  {t(language, 'Nutrition information —')} {msg.foodData.nutritionInformation.source}
                                  {msg.foodData.nutritionInformation.dataType && ` (${t(language, msg.foodData.nutritionInformation.dataType)})`}
                                </h4>
                                <p className="mt-1 text-xs text-slate-600">
                                  {t(language, 'Values come from this database record. Check its source and serving details; the values may not match every brand or recipe.')}
                                </p>
                                {Object.keys(msg.foodData.nutritionInformation.per100g || {}).length > 0 ? (
                                  <ul className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
                                    {Object.entries(msg.foodData.nutritionInformation.per100g).map(([name, nutrient]) => (
                                      <li key={name} className="rounded-md border border-slate-100 p-2 text-sm text-slate-800">
                                        <strong className="capitalize">{t(language, name.replace(/([A-Z])/g, ' $1'))}</strong>: {nutrient.value} {nutrient.unit}
                                        {NUTRIENT_EXPLANATIONS[name] && (
                                          <span className="mt-0.5 block text-xs text-slate-600">
                                            {t(language, NUTRIENT_EXPLANATIONS[name])}
                                          </span>
                                        )}
                                      </li>
                                    ))}
                                  </ul>
                                ) : (
                                  <p className="mt-2 text-sm text-slate-600">
                                    {t(language, 'No nutrient values were provided for this database record.')}
                                  </p>
                                )}
                              </div>
                            )}
                            {msg.foodData.productInfo?.nutritionPer100g && Object.keys(msg.foodData.productInfo.nutritionPer100g).length > 0 && (
                              <div className="rounded-lg bg-white/80 p-3 text-sm text-slate-700">
                                <h4 className="font-semibold text-slate-800">
                                  {t(language, 'Product-label nutrition — Open Food Facts catalog')}
                                </h4>
                                <p className="mt-1 text-xs text-slate-600">
                                  {t(language, 'These community-submitted values may not match the package. Check the label on your product.')}
                                </p>
                                <ul className="mt-2 grid grid-cols-1 gap-1 sm:grid-cols-2">
                                  {Object.entries(msg.foodData.productInfo.nutritionPer100g).map(([name, value]) => (
                                    <li key={name}>{t(language, name.replace(/([A-Z])/g, ' $1'))}: {value}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {!msg.foodData.webInformation && !msg.foodData.productInfo && !msg.foodData.nutritionInformation && (
                              <p className="text-sm text-slate-700">
                                {t(language, 'Live data was unavailable for this search. Use the direct links below to look up this food on other sites.')}
                              </p>
                            )}
                            <p className="text-xs text-slate-500">
                              {t(language, 'Online references may be incomplete or out of date. They describe reference records and do not verify the specific food you have.')}
                            </p>
                            <div className="flex flex-wrap gap-2 border-t border-sky-200 pt-3">
                              {getFoodReferenceLinks(msg.foodData.foodName).map((source) => (
                                <a
                                  key={source.name}
                                  href={source.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-1 rounded-lg border border-sky-200 bg-white px-3 py-1.5 text-xs font-semibold text-sky-800 hover:bg-sky-100"
                                >
                                  {source.name}<ExternalLink className="h-3 w-3" />
                                </a>
                              ))}
                            </div>
                          </section>

                          {/* 1. Common Adulterants */}
                          <div className="space-y-1.5">
                            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                              <span>1. {t(language, 'Possible adulterants (risk indicators, not a sample result)')}</span>
                            </h3>
                            <ul className="list-disc list-inside space-y-1 text-slate-800 text-[14px]">
                              {(msg.foodData.adulterants || []).map((item, idx) => (
                                <li key={idx}><span className="font-semibold text-slate-900">{t(language, item)}</span></li>
                              ))}
                            </ul>
                          </div>

                          {/* 2. Why Adulteration Occurs */}
                          <div className="space-y-1">
                            <h3 className="font-bold text-slate-900 text-base">
                              2. {t(language, 'Motivation for Adulteration')}
                            </h3>
                            <p className="text-slate-700 text-[14px] leading-relaxed">
                              {t(language, msg.foodData.whyAdulterated)}
                            </p>
                          </div>

                          {/* 3. Awareness Check */}
                          <div className="space-y-2 bg-emerald-50/50 border border-emerald-200/80 p-4 rounded-xl">
                            <h3 className="font-bold text-emerald-950 text-base flex items-center gap-2">
                              <span>🧪 3. {t(language, 'Preliminary Awareness Test Method')}</span>
                            </h3>
                            <p className="text-[14px] text-slate-800">
                              <strong>{t(language, 'Check:')} </strong>{t(language, msg.foodData.testMethod)}
                            </p>
                            {msg.foodData.testProcedure && (
                              <div className="text-[14px] text-slate-700 bg-white p-3 rounded-lg border border-emerald-200">
                                <strong>{t(language, 'Step-by-step Procedure:')}</strong>
                                <ol className="list-decimal list-inside mt-2 space-y-1">
                                  {msg.foodData.testProcedure.split(/\r?\n/).filter(Boolean).map((step, idx) => (
                                    <li key={idx}>{t(language, step.replace(/^\s*\d+[.)]\s*/, ''))}</li>
                                  ))}
                                </ol>
                              </div>
                            )}
                            <p className="text-[14px] text-slate-800">
                              <strong>{t(language, 'Expected Result:')} </strong>{t(language, msg.foodData.observation)}
                            </p>
                            <div className="text-[12px] text-amber-900 bg-amber-50 p-2.5 rounded border border-amber-200 mt-2 font-medium">
                              ⚠️ <em><strong>{t(language, 'Advisory:')}</strong> {t(language, 'This is a preliminary household awareness check. Certified laboratory testing is required for scientific legal confirmation. Do not consume tested food portions.')}</em>
                            </div>
                          </div>

                          {/* 4. Health Concerns */}
                          <div className="space-y-1.5">
                            <h3 className="font-bold text-slate-900 text-base">
                              4. {t(language, 'Potential Health Hazards')}
                            </h3>
                            <ul className="list-disc list-inside space-y-1 text-slate-800 text-[14px]">
                              {(msg.foodData.healthRisks || []).map((risk, idx) => (
                                <li key={idx}>{t(language, risk)}</li>
                              ))}
                            </ul>
                          </div>

                          {/* 5. Safe Buying Tips */}
                          <div className="space-y-1.5">
                            <h3 className="font-bold text-slate-900 text-base">
                              5. 🛒 {t(language, 'Safe Purchasing Recommendations')}
                            </h3>
                            <ul className="list-disc list-inside space-y-1 text-slate-800 text-[14px]">
                              {(msg.foodData.safeTips || []).map((tip, idx) => (
                                <li key={idx}>{t(language, tip)}</li>
                              ))}
                            </ul>
                          </div>

                          {/* 6. Storage Tips */}
                          <div className="space-y-1.5">
                            <h3 className="font-bold text-slate-900 text-base">
                              6. 📦 {t(language, 'Proper Storage Guidelines')}
                            </h3>
                            <ul className="list-disc list-inside space-y-1 text-slate-800 text-[14px]">
                              {(msg.foodData.storageTips || []).map((tip, idx) => (
                                <li key={idx}>{t(language, tip)}</li>
                              ))}
                            </ul>
                          </div>

                          {/* 7. Official Sources */}
                          <div className="space-y-1 pt-2 border-t border-slate-200 text-xs text-slate-600">
                            <strong>{t(language, 'Food safety sources and references:')}</strong>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {(msg.foodData.sources || []).map((s, idx) => (
                                <a
                                  key={idx}
                                  href={s.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-1 text-emerald-700 hover:text-emerald-900 font-medium underline"
                                >
                                  <span>{s.name}</span>
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              ))}
                            </div>
                          </div>

                        </div>
                      )}

                      {/* Action Icons below response */}
                      <div className="flex items-center gap-1 text-slate-400 text-xs pt-1">
                        <button
                          onClick={() => handleCopy(msg.id, msg.foodData && !msg.isFoodFollowUp ? getFoodSummaryText(msg.foodData) : msg.content)}
                          className="p-1.5 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                          title={t(language, 'Copy response')}
                        >
                          {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>

                        <button
                          onClick={() => handleSpeak(msg.id, msg.foodData && !msg.isFoodFollowUp ? getFoodSummaryText(msg.foodData) : msg.content)}
                          className="p-1.5 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                          title={t(language, 'Read aloud')}
                        >
                          {speakingId === msg.id ? <VolumeX className="w-3.5 h-3.5 text-rose-600" /> : <Volume2 className="w-3.5 h-3.5" />}
                        </button>

                        <button
                          className="p-1.5 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                          title={t(language, 'Helpful analysis')}
                        >
                          <ThumbsUp className="w-3.5 h-3.5" />
                        </button>

                        <button
                          className="p-1.5 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                          title={t(language, 'Report concern')}
                        >
                          <ThumbsDown className="w-3.5 h-3.5" />
                        </button>

                        <button
                          onClick={() => handleSend(messages[messages.length - 2]?.content || 'Milk')}
                          className="p-1.5 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                          title={t(language, 'Re-analyze')}
                        >
                          <RotateCcw className="w-3.5 h-3.5" />
                        </button>
                      </div>

                    </div>
                  )}

                </div>
              ))}

              {/* Typing / Loading indicator */}
              {loading && (
                <div className="flex gap-2 items-center text-xs text-slate-500 py-2">
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce" />
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:0.2s]" />
                  <div className="w-2 h-2 rounded-full bg-emerald-600 animate-bounce [animation-delay:0.4s]" />
                  <span className="font-mono text-emerald-800 ml-1">{t(language, 'Analyzing food safety data & certified tests...')}</span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {/* 3. Centered Floating Pill Input Bar */}
          <div className="w-full pb-4 sm:pb-6 relative">
            
            {/* Quick Food Staples Selector */}
            {quickMenuOpen && (
              <div className="absolute bottom-20 left-0 bg-white border border-slate-200 rounded-2xl p-3 shadow-xl z-30 max-w-xs animate-fadeIn">
                <div className="text-[11px] font-bold uppercase text-emerald-700 mb-2 px-1">
                  {t(language, 'Common Food Commodities')}
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  {[
                    { name: 'Milk', icon: '🥛' },
                    { name: 'Turmeric', icon: '🌶️' },
                    { name: 'Chilli Powder', icon: '🌶️' },
                    { name: 'Honey', icon: '🍯' },
                    { name: 'Sugar', icon: '🍚' },
                    { name: 'Ghee', icon: '🧈' },
                    { name: 'Edible Oil', icon: '🛢️' },
                    { name: 'Rice', icon: '🌾' },
                  ].map((item) => (
                    <button
                      key={item.name}
                      onClick={() => {
                        setQuickMenuOpen(false);
                        handleSend(item.name);
                      }}
                      className="flex items-center gap-1.5 p-2 rounded-lg hover:bg-emerald-50 text-xs font-semibold text-slate-800 transition-colors"
                    >
                      <span>{item.icon}</span>
                      <span>{t(language, item.name)}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {foodSuggestions.length > 0 && (
              <div
                role="listbox"
                aria-label="Food suggestions"
                className="absolute bottom-16 left-0 right-0 z-40 max-h-72 overflow-y-auto rounded-2xl border border-slate-200 bg-white p-2 shadow-xl"
              >
                <p className="px-3 py-2 text-[11px] font-semibold text-slate-500">
                  Select a food to view its product and safety details
                </p>
                {foodSuggestions.map((food) => (
                  <button
                    key={food.foodName}
                    type="button"
                    role="option"
                    aria-selected="false"
                    onClick={() => handleSend(food.foodName)}
                    className="flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-left hover:bg-emerald-50 focus:bg-emerald-50 focus:outline-none"
                  >
                    <span className="font-semibold text-sm text-slate-800">
                      {food.foodName}
                    </span>
                    <span className="text-xs text-slate-500">
                      {food.category || 'Food item'}
                    </span>
                  </button>
                ))}
              </div>
            )}

            {/* Pill Container */}
            <div className="flex items-center bg-white rounded-full border border-slate-300 shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:shadow-md focus-within:shadow-md focus-within:border-emerald-500 transition-all px-3 py-2">
              
              {/* + Quick Staples Button */}
              <button
                onClick={() => setQuickMenuOpen(!quickMenuOpen)}
                className="p-1.5 text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 rounded-full transition-colors mr-1"
                title={t(language, 'Quick food staples menu')}
              >
                <Plus className="w-5 h-5 stroke-[2]" />
              </button>

              {/* Text Input with Unique Placeholder */}
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder={t(language, 'Ask about food safety, adulteration checks, or test methods (e.g. Milk, Turmeric, Honey)...')}
                className="flex-1 bg-transparent py-1.5 px-2 text-[14px] sm:text-[15px] text-[#0d0d0d] placeholder:text-slate-400 focus:outline-none"
              />

              {/* Microphone Icon Button */}
              <button
                onClick={handleVoiceInput}
                type="button"
                className={`p-1.5 rounded-full transition-colors mr-1 ${
                  isListening ? 'text-rose-600 bg-rose-50 animate-pulse' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
                }`}
                title={t(language, 'Voice inquiry')}
              >
                {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
              </button>

              {/* Circular Send Button */}
              <button
                onClick={() => handleSend()}
                disabled={loading || !inputValue.trim()}
                className="w-8 h-8 rounded-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-30 disabled:hover:bg-emerald-600 text-white flex items-center justify-center transition-all shrink-0 shadow-xs"
                title={t(language, 'Analyze food safety')}
              >
                <ArrowRight className="w-4 h-4" />
              </button>

            </div>

          </div>

        </main>

      </div>

      {/* FSSAI & AGMARK Standards Modal */}
      {standardsModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2 text-emerald-800 font-extrabold text-base">
                <BookOpen className="w-5 h-5 text-emerald-600" />
                <span>{t(language, 'Certified Food Safety Standards')}</span>
              </div>
              <button 
                onClick={() => setStandardsModalOpen(false)}
                className="text-slate-400 hover:text-slate-700 font-bold text-lg"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3 text-xs sm:text-sm text-slate-700 max-h-96 overflow-y-auto">
              <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200">
                <strong className="text-emerald-950 block mb-1">{t(language, 'FSSAI (Food Safety and Standards Authority of India):')}</strong>
                {t(language, 'Mandates 14-digit license number and Food Safety Logo on all manufactured food products.')}
              </div>
              <div className="p-3 bg-teal-50 rounded-xl border border-teal-200">
                <strong className="text-teal-950 block mb-1">{t(language, 'AGMARK Certification:')}</strong>
                {t(language, 'Quality grade certification for agricultural products including pure honey, ghee, and edible spices.')}
              </div>
              <div className="p-3 bg-blue-50 rounded-xl border border-blue-200">
                <strong className="text-blue-950 block mb-1">{t(language, 'Jaago Grahak Jaago Guidelines:')}</strong>
                {t(language, 'Encourages consumers to demand sealed packaging and report adulterated food to local food inspectors.')}
              </div>
            </div>
            <div className="text-right">
              <button
                onClick={() => setStandardsModalOpen(false)}
                className="px-4 py-2 bg-emerald-600 text-white text-xs font-bold rounded-xl hover:bg-emerald-700"
              >
                {t(language, 'Close Standards Guide')}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
