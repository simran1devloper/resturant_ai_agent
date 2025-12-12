import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, ShoppingBag, Info, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const API_BASE = 'http://localhost:8005';

function App() {
  const [menu, setMenu] = useState([]);
  const [cart, setCart] = useState({});
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your AI food assistant. Ask me anything about our menu or ingredients!' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('menu'); // menu | chat

  useEffect(() => {
    fetchMenu();
  }, []);

  const fetchMenu = async () => {
    try {
      const res = await axios.get(`${API_BASE}/menu/all`);
      setMenu(res.data);
    } catch (err) {
      console.error("Failed to fetch menu", err);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.get(`${API_BASE}/rag/query`, { params: { q: userMsg } });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.content }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const addToCart = async (item) => {
    try {
      setCart(prev => ({
        ...prev,
        [item.name]: (prev[item.name] || 0) + 1
      }));
      await axios.post(`${API_BASE}/order/create`, { item: item.name, quantity: 1 });
    } catch (err) {
      console.error("Failed to order", err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/80 border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center transform rotate-3">
              <ShoppingBag className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
              Gourmet AI
            </h1>
          </div>

          <nav className="flex gap-1 bg-white/5 p-1 rounded-full">
            <button
              onClick={() => setActiveTab('menu')}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${activeTab === 'menu' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-400 hover:text-white'}`}
            >
              Menu
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${activeTab === 'chat' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-400 hover:text-white'}`}
            >
              AI Assistant
            </button>
          </nav>

          <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center border border-white/5">
            <span className="text-xs font-bold">{Object.values(cart).reduce((a, b) => a + b, 0)}</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {activeTab === 'menu' ? (
            <motion.div
              key="menu"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {menu.length > 0 ? (
                menu.map((item, idx) => (
                  <div key={idx} className="group relative bg-slate-900/50 border border-white/5 rounded-2xl overflow-hidden hover:border-indigo-500/30 transition-all hover:shadow-2xl hover:shadow-indigo-500/10">
                    <div className="aspect-video bg-slate-800 relative overflow-hidden">
                      <img
                        src={`https://source.unsplash.com/800x600/?${item.name.replace(' ', '-')},food`}
                        alt={item.name}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                        onError={(e) => e.target.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80'}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent opacity-60" />
                    </div>
                    <div className="p-5">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-lg font-semibold text-white group-hover:text-indigo-400 transition-colors">{item.name}</h3>
                        <span className="bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded-md text-sm font-mono">${item.price || '12.99'}</span>
                      </div>
                      <p className="text-slate-400 text-sm mb-4 line-clamp-2">{item.ingredients || 'Delicious ingredients prepared by our chef.'}</p>
                      <button
                        onClick={() => addToCart(item)}
                        className="w-full py-2.5 rounded-xl bg-white/5 hover:bg-indigo-600 text-white font-medium transition-all flex items-center justify-center gap-2 border border-white/5 hover:border-transparent group-hover:shadow-lg group-hover:shadow-indigo-500/20"
                      >
                        <ShoppingBag className="w-4 h-4" /> Add to Order
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-span-full flex flex-col items-center justify-center py-20 text-slate-500">
                  <Loader2 className="w-8 h-8 animate-spin mb-4" />
                  <p>Loading menu...</p>
                </div>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="chat"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="max-w-2xl mx-auto h-[600px] flex flex-col bg-slate-900/50 border border-white/5 rounded-3xl overflow-hidden shadow-2xl relative"
            >
              {/* Chat Gradient Background */}
              <div className="absolute inset-0 bg-gradient-to-b from-indigo-500/5 to-purple-500/5 pointer-events-none" />

              <div className="flex-1 overflow-y-auto p-6 space-y-4 scroll-smooth relative z-10">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div
                      className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${msg.role === 'user'
                          ? 'bg-indigo-600 text-white rounded-br-none shadow-lg shadow-indigo-600/20'
                          : 'bg-white/10 text-slate-200 rounded-bl-none backdrop-blur-sm markdown-content'
                        }`}
                    >
                      {msg.role === 'user' ? (
                        msg.content
                      ) : (
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            table: ({ node, ...props }) => (
                              <table className="w-full border-collapse border border-white/20 my-2 rounded" {...props} />
                            ),
                            thead: ({ node, ...props }) => (
                              <thead className="bg-white/5" {...props} />
                            ),
                            th: ({ node, ...props }) => (
                              <th className="border border-white/20 px-3 py-2 text-left font-semibold text-white" {...props} />
                            ),
                            td: ({ node, ...props }) => (
                              <td className="border border-white/20 px-3 py-2" {...props} />
                            ),
                            h1: ({ node, ...props }) => (
                              <h1 className="text-xl font-bold mt-4 mb-2 text-white" {...props} />
                            ),
                            h2: ({ node, ...props }) => (
                              <h2 className="text-lg font-bold mt-3 mb-2 text-white" {...props} />
                            ),
                            h3: ({ node, ...props }) => (
                              <h3 className="text-base font-semibold mt-2 mb-1 text-white" {...props} />
                            ),
                            code: ({ node, inline, ...props }) =>
                              inline ? (
                                <code className="bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded text-xs" {...props} />
                              ) : (
                                <code className="block bg-slate-900/50 p-2 rounded mt-1 mb-1 text-xs" {...props} />
                              ),
                            ul: ({ node, ...props }) => (
                              <ul className="list-disc list-inside my-2 space-y-1" {...props} />
                            ),
                            ol: ({ node, ...props }) => (
                              <ol className="list-decimal list-inside my-2 space-y-1" {...props} />
                            ),
                            p: ({ node, ...props }) => (
                              <p className="my-1.5 leading-relaxed" {...props} />
                            ),
                            strong: ({ node, ...props }) => (
                              <strong className="font-semibold text-white" {...props} />
                            ),
                            em: ({ node, ...props }) => (
                              <em className="italic" {...props} />
                            ),
                            blockquote: ({ node, ...props }) => (
                              <blockquote className="border-l-2 border-indigo-500/50 pl-3 my-2 italic text-slate-300" {...props} />
                            ),
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      )}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white/5 p-4 rounded-2xl rounded-bl-none flex gap-1">
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.1s]" />
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                    </div>
                  </div>
                )}
              </div>

              <div className="p-4 bg-slate-950/50 border-t border-white/5 backdrop-blur-md relative z-10">
                <form
                  onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}
                  className="flex gap-2"
                >
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about our special pasta..."
                    className="flex-1 bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all placeholder:text-slate-600"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="bg-indigo-600 hover:bg-indigo-500 text-white p-3 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-600/20"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </form>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
