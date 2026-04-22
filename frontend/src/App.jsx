import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, TrendingUp, LogOut, Lock, User, PlusCircle, AlertCircle, Database, Mail } from 'lucide-react';

function App() {
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [assets, setAssets] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Auth states
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // New Asset states
  const [symbol, setSymbol] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [currentPrice, setCurrentPrice] = useState('');
  
  const API_URL = 'http://localhost:8000/api/v1';

  const authSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const endpoint = isRegistering ? 'register/' : 'login/';
    const bodyArgs = isRegistering 
      ? { username, email, password, role: 'USER' } 
      : { username, password };

    try {
      // 1. Submit Registration or Login
      const res = await fetch(`${API_URL}/auth/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyArgs)
      });
      const data = await res.json();
      
      if (res.ok) {
        if (isRegistering) {
            // Auto login after fast registration
            const loginRes = await fetch(`${API_URL}/auth/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const loginData = await loginRes.json();
            if(loginRes.ok) {
               localStorage.setItem('access_token', loginData.access);
               setToken(loginData.access);
               setError('');
            }
        } else {
            localStorage.setItem('access_token', data.access);
            setToken(data.access);
            setError('');
        }
      } else {
        // DRF Standard errors usually return lists or dictionaries
        setError(JSON.stringify(data));
      }
    } catch (err) {
      setError('Network connection error. Check backend link.');
    }
    setLoading(false);
  };

  const fetchWatchlist = async () => {
    try {
      const res = await fetch(`${API_URL}/watchlist/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) {
        setAssets(data.results || data);
      } else if (res.status === 401) {
        setToken(null);
        localStorage.removeItem('access_token');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const addAsset = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/watchlist/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          symbol: symbol.toUpperCase(),
          target_price: targetPrice,
          current_price: currentPrice
        })
      });
      if (res.ok) {
         setSymbol('');
         setTargetPrice('');
         setCurrentPrice('');
         fetchWatchlist();
      } else {
         const data = await res.json();
         setError("Error adding asset: Values must be positive.");
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (token) fetchWatchlist();
  }, [token]);

  const getRiskIcon = (level) => {
    if (level === 'HIGH') return <ShieldAlert size={16} />;
    if (level === 'MEDIUM') return <AlertCircle size={16} />;
    return <TrendingUp size={16} />;
  };

  if (!token) {
    return (
      <div className="login-wrapper">
        <div className="login-glow"></div>
        <div className="glass-card animate-fade-in" style={{width: '400px'}}>
          <div style={{textAlign: 'center', marginBottom: '2rem'}}>
            <Activity color="var(--accent-cyan)" size={48} style={{marginBottom: '1rem'}} />
            <h2 className="gradient-text" style={{fontSize: '2rem'}}>Trading Pulse</h2>
            <p style={{color: 'var(--text-secondary)'}}>Secure Risk Intelligence Engine</p>
          </div>

          {error && (
            <div style={{background: 'rgba(255, 51, 102, 0.1)', borderLeft: '4px solid #ff3366', padding: '1rem', borderRadius: '4px', marginBottom: '1.5rem', color: '#ff3366', fontSize: '0.8rem', display: 'flex', alignItems: 'flex-start', gap: '0.5rem', overflowWrap: 'anywhere'}}>
              <AlertCircle size={16} style={{flexShrink: 0}} /> {error.replace(/[{}"\[\]]/g,' ')}
            </div>
          )}

          <form onSubmit={authSubmit}>
            <div className="input-group">
              <User className="input-icon" size={20} />
              <input type="text" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} required />
            </div>
            
            {isRegistering && (
              <div className="input-group">
                <Mail className="input-icon" size={20} />
                <input type="email" placeholder="Email Address" value={email} onChange={e=>setEmail(e.target.value)} required />
              </div>
            )}

            <div className="input-group">
              <Lock className="input-icon" size={20} />
              <input type="password" placeholder="Password (min 8 chars)" value={password} onChange={e=>setPassword(e.target.value)} required />
            </div>
            
            <button type="submit" className="btn-glow" disabled={loading} style={{marginTop: '2rem'}}>
              {loading ? <div className="spinner" /> : (isRegistering ? 'Create Secure Account' : 'Authenticate Core')}
            </button>
          </form>

          <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
             <span style={{color: 'var(--text-secondary)', fontSize: '0.9rem', cursor:'pointer'}} onClick={() => {setIsRegistering(!isRegistering); setError('');}}>
               {isRegistering ? 'Already have an operating core? Login here' : 'Need clearance? Register here'}
             </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-layout animate-fade-in">
      <nav className="navbar">
        <div className="logo-container">
          <Activity color="var(--accent-cyan)" size={32} />
          <h2 className="gradient-text">Trading Pulse OS</h2>
        </div>
        <button className="btn-secondary" onClick={() => { setToken(null); localStorage.removeItem('access_token'); }}>
          <LogOut size={16} /> Disconnect API
        </button>
      </nav>

      <div style={{display: 'flex', gap: '2rem', marginTop: '1rem'}}>
        {/* Left Action Panel */}
        <div style={{flex: '1'}}>
          <div className="glass-card panel-card">
            <h3><TrendingUp style={{display: 'inline', verticalAlign: 'text-bottom', color: 'var(--accent-cyan)', marginRight: '0.5rem'}}/> Command Asset Engine</h3>
            <p className="insight-text" style={{marginBottom: '1.5rem'}}>Inject a new ticker to evaluate real-time differential risk logic.</p>
            
            <form onSubmit={addAsset}>
               <div className="input-group">
                 <Database className="input-icon" size={18} />
                 <input placeholder="Asset Ticker (e.g. SOLUSDT)" value={symbol} onChange={e=>setSymbol(e.target.value)} required />
               </div>
               
               <div style={{display: 'flex', gap: '1rem'}}>
                 <div className="input-group" style={{flex: 1}}>
                    <input type="number" step="0.01" placeholder="Current Quote" value={currentPrice} onChange={e=>setCurrentPrice(e.target.value)} required style={{paddingLeft: '1rem'}} />
                 </div>
                 <div className="input-group" style={{flex: 1}}>
                    <input type="number" step="0.01" placeholder="Target Matrix" value={targetPrice} onChange={e=>setTargetPrice(e.target.value)} required style={{paddingLeft: '1rem'}} />
                 </div>
               </div>

               {error && <p style={{color: 'var(--risk-high)', fontSize: '0.85rem'}}>{error}</p>}

               <button type="submit" className="btn-glow" disabled={loading} style={{padding: '0.8rem', marginTop: '0.5rem'}}>
                 {loading ? <div className="spinner" /> : <><PlusCircle size={18} /> INJECT ASSET</>}
               </button>
            </form>
          </div>
        </div>

        {/* Right Data Panel */}
        <div style={{flex: '2'}}>
          <div className="glass-card">
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <h3>Active Radar Matrix</h3>
              <div className="risk-badge risk-high" style={{fontSize: '0.7rem'}}>Live Tracking</div>
            </div>
            
            {assets.length === 0 ? (
              <div style={{textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-secondary)'}}>
                <Database opacity={0.2} size={64} style={{margin: '0 auto 1rem'}} />
                <p>System operational, but data matrix is empty.</p>
                <p>Awaiting asset injection...</p>
              </div>
            ) : (
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Ticker</th>
                      <th>Market Quote</th>
                      <th>Target Execution</th>
                      <th>Risk Engine Assessment</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assets.map(asset => {
                      const level = asset.risk_analysis?.risk_level || 'UNKNOWN';
                      const lowerLevel = level.toLowerCase();
                      return (
                        <tr key={asset.id}>
                          <td className="asset-symbol">{asset.symbol}</td>
                          <td className="price-text">${parseFloat(asset.current_price).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                          <td className="price-text">${parseFloat(asset.target_price).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                          <td>
                            <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                              <div>
                                <span className={`risk-badge risk-${lowerLevel}`}>
                                  {getRiskIcon(level)} {level} • SCO: {asset.risk_analysis?.risk_score}
                                </span>
                              </div>
                              <div className="insight-text">{asset.risk_analysis?.insight}</div>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default App;
