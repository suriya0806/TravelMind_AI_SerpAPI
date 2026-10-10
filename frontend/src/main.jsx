import React,{useState} from "react";
import {createRoot} from "react-dom/client";
import {Plane,Hotel,MapPin,Wallet,Compass,User,Home,CalendarDays,Route,CloudRain, Sparkles, Check, Loader2, ChevronRight, Navigation, RefreshCw, ShieldCheck} from "lucide-react";
import "./styles.css";

const API="http://localhost:8000";
const initial={origin:"Chennai",destination:"Goa",start_date:"2026-10-12",end_date:"2026-10-15",travellers:2,budget:25000,interests:["Food","Photography","Culture"]};

function App(){
 const [form,setForm]=useState(initial),[page,setPage]=useState("home"),[trip,setTrip]=useState(null),[loading,setLoading]=useState(false),[active,setActive]=useState("Overview"),[toast,setToast]=useState("");
 const interests=["Food","Beaches","Photography","Adventure","Shopping","Culture"];
 const plan=async()=>{setLoading(true);setPage("planning");try{let r=await fetch(API+"/api/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(form)});setTrip(await r.json());setTimeout(()=>{setLoading(false);setPage("trip")},1200)}catch(e){setLoading(false);setToast("Start the FastAPI backend first.");}};
 const whatIf=async(s,v)=>{setToast("AI is re-optimizing every connected module…");let r=await fetch(API+"/api/what-if",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({trip:form,scenario:s,value:v})});setTrip(await r.json());setActive("Overview");setTimeout(()=>setToast("Plan updated across itinerary, route and budget."),900)};
 const nav=(p)=>{if(!trip&&p!=="home")return;setPage(p)};
 return <div className="app">
  <header><div className="brand" onClick={()=>nav("home")}><div className="logo"><Sparkles/></div><div>TRAVELMIND <span>AI</span><small>AI TRAVEL OPERATING SYSTEM</small></div></div>
   <nav>{["Explore","Trips","Discover"].map(x=><button onClick={()=>nav(x.toLowerCase())} className={page===x.toLowerCase()?"navActive":""}>{x}</button>)}</nav><button className="profile"><User size={17}/> Profile</button>
  </header>
  <main>
   {page==="home"&&<HomePage form={form} setForm={setForm} interests={interests} plan={plan}/>}
   {page==="planning"&&<Planning/>}
   {page!=="home"&&page!=="planning"&&trip&&<TripShell trip={trip} active={active} setActive={setActive} whatIf={whatIf}/>}
  </main>
  {toast&&<div className="toast">{toast}</div>}
 </div>
}

function HomePage({form,setForm,interests,plan}){
 const toggle=i=>setForm({...form,interests:form.interests.includes(i)?form.interests.filter(x=>x!==i):[...form.interests,i]});
 return <section className="home">
  <div className="hero"><div className="eyebrow"><Sparkles size={15}/> PERSONALIZED BY MULTIPLE AI AGENTS</div><h1>Your entire trip,<br/><em>planned by AI.</em></h1><p>Flights, hotels, places, routes and experiences — intelligently combined into one personalized journey.</p></div>
  <div className="planner card">
   <div className="field wide"><label>WHERE DO YOU WANT TO GO?</label><div className="input">📍 <input value={form.origin} onChange={e=>setForm({...form,origin:e.target.value})}/><span>→</span><input value={form.destination} onChange={e=>setForm({...form,destination:e.target.value})}/></div></div>
   <div className="field"><label>WHEN?</label><div className="input">📅 <input type="date" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})}/><span>→</span><input type="date" value={form.end_date} onChange={e=>setForm({...form,end_date:e.target.value})}/></div></div>
   <div className="field"><label>TRAVELLERS</label><div className="input">👥 <input type="number" min="1" value={form.travellers} onChange={e=>setForm({...form,travellers:+e.target.value})}/><span>Adults</span></div></div>
   <div className="field"><label>BUDGET</label><div className="input">₹ <input type="number" value={form.budget} onChange={e=>setForm({...form,budget:+e.target.value})}/></div></div>
   <div className="field wide"><label>WHAT DO YOU LIKE?</label><div className="chips">{interests.map(i=><button className={form.interests.includes(i)?"chip on":"chip"} onClick={()=>toggle(i)}>{form.interests.includes(i)?"✓":"＋"} {i}</button>)}</div></div>
   <button className="planBtn" onClick={plan}><Sparkles/> PLAN MY TRIP <ChevronRight/></button>
  </div>
  <div className="discoverRow"><div><span className="muted">POPULAR WITH TRAVELLERS</span><div className="destinations">{["Goa","Kerala","Dubai","Singapore"].map(x=><button>{x} ↗</button>)}</div></div><div className="surprise"><Sparkles/><div><b>Let AI decide</b><small>“I have ₹15,000 and 3 days. Surprise me.”</small></div><ChevronRight/></div></div>
 </section>
}
function Planning(){const agents=[["✈️","Flight Agent"],["🏨","Hotel Agent"],["📍","Discovery Agent"],["🗺️","Route Agent"],["💰","Budget Agent"],["🛡️","Safety Agent"],["🧠","Itinerary Agent"]];return <section className="planning"><div className="spinner"><Sparkles/></div><h1>TravelMind is <em>planning</em> your trip...</h1><p>Multiple specialized agents are researching, comparing and optimizing your journey.</p><div className="agentGrid">{agents.map((a,i)=><div className="agent"><span>{a[0]}</span><div><b>{a[1]}</b><small><Check size={12}/> Done</small></div></div>)}</div></section>}
function TripShell({trip,active,setActive,whatIf}){const tabs=[["Overview",Compass],["Flights",Plane],["Hotel",Hotel],["Places",MapPin],["Map",Route],["Itinerary",CalendarDays],["Budget",Wallet],["Live Trip",Navigation]];return <section className="trip">
 <div className="tripHead"><div><span className="eyebrow">YOUR AI-GENERATED JOURNEY</span><h1>{trip.request.destination}<span> · {trip.request.start_date} — {trip.request.end_date}</span></h1></div><div className="live"><i/> TRIP READY</div></div>
 <div className="tabs">{tabs.map(([x,I])=><button className={active===x?"tab active":"tab"} onClick={()=>setActive(x)}><I size={16}/>{x}</button>)}</div>
 <div className="content">{active==="Overview"&&<Overview trip={trip} whatIf={whatIf}/>}
 {active==="Flights"&&<Flights trip={trip}/>} {active==="Hotel"&&<HotelPage trip={trip}/>}
 {active==="Places"&&<Places trip={trip}/>} {active==="Map"&&<MapPage trip={trip}/>}
 {active==="Itinerary"&&<Itinerary trip={trip}/>} {active==="Budget"&&<Budget trip={trip} whatIf={whatIf}/>}
 {active==="Live Trip"&&<Live trip={trip}/>}</div>
 </section>}
const Card=({children,cls=""})=><div className={"card "+cls}>{children}</div>;
function Overview({trip,whatIf}){return <div className="overview"><div className="grid2"><Card><div className="sectionTitle"><span>✈️</span><div><b>Best flight</b><small>AI-selected for your itinerary</small></div></div><h2>Air India <strong>₹6,240</strong></h2><p>Chennai → Goa · 08:30 — 10:55 · 2h 25m</p><div className="aiNote">🧠 <b>Why we chose this:</b> It arrives early enough to preserve 4 hours of your Day 1 itinerary.</div></Card>
 <Card><div className="sectionTitle"><span>🏨</span><div><b>Recommended hotel</b><small>Best balance of value + location</small></div></div><h2>Ocean View Resort <strong>₹2,100<small>/night</small></strong></h2><p>⭐ 4.5 · 1.2 km from planned attractions</p><div className="aiNote">🧠 <b>AI decision:</b> ₹600 cheaper than the highest-rated option and cuts daily travel time.</div></Card></div>
 <div className="grid3"><Metric icon="🗺️" title="Route" value="42 min" sub="24 min saved"/><Metric icon="💰" title="Budget" value={"₹"+trip.budget.total.toLocaleString()} sub={trip.budget.remaining>=0?"₹"+trip.budget.remaining.toLocaleString()+" remaining":"Over budget"}/><Metric icon="📍" title="Discoveries" value={trip.places.length} sub="2 hidden gems"/></div>
 <Card><div className="cardHead"><div><span className="eyebrow">WHAT-IF SIMULATOR</span><h2>See how AI adapts to change.</h2></div><button className="outline" onClick={()=>whatIf("Budget reduced to ₹18,000",18000)}>💰 Budget → ₹18K</button><button className="outline" onClick={()=>whatIf("Rain expected tomorrow")}>☔ Rain tomorrow</button></div><p className="muted">Change one condition and TravelMind recalculates hotel, activities, routes and itinerary together.</p></Card>
 </div>}
function Metric({icon,title,value,sub}){return <Card cls="metric"><span>{icon}</span><small>{title}</small><b>{value}</b><em>{sub}</em></Card>}
function Flights({trip}){return <div><PageTitle title="Best Flights for Your Trip" sub="Ranked by price, arrival time and itinerary impact."/>{trip.flights.map(f=><Card cls="result"><div className="bigIcon">✈️</div><div className="grow"><b>{f.airline}</b><small>{f.from} → {f.to}</small><div className="times">{f.depart} → {f.arrive} <span>{f.duration}</span></div></div><div><span className="tag">{f.tag}</span><h2>₹{f.price.toLocaleString()}</h2><button className="primary">Select</button></div></Card>)}<Card cls="aiNote">🧠 <b>AI Recommendation:</b> The ₹6,240 option is the best-value choice for the complete trip.</Card></div>}
function HotelPage({trip}){return <div><PageTitle title="Stay selected for your journey" sub="Hotels are scored using price, rating, location and route impact."/><div className="hotelGrid">{trip.hotels.map(h=><Card><div className="hotelImg">🏨</div><span className="tag">⭐ {h.rating}</span><h2>{h.name}</h2><p>{h.distance} from your planned attractions</p><div className="amen">{h.amenities.map(a=><span>✓ {a}</span>)}</div><h3>₹{h.night.toLocaleString()} <small>/night</small></h3><div className="aiNote">🧠 {h.reason}</div></Card>)}</div></div>}
function Places({trip}){return <div><PageTitle title="Discover places made for you" sub="Popular spots plus hidden gems discovered by AI."/><div className="placeGrid">{trip.places.map(p=><Card><div className="placeTop"><span className="placeEmoji">{p.category==="Food"?"🍛":p.category==="Photography"?"📸":p.category==="Culture"?"🏛️":"🏖️"}</span><span className={p.type==="hidden"?"tag purple":"tag"}>{p.type==="hidden"?"✨ Hidden Gem":"Popular"}</span></div><h2>{p.name}</h2><p>⭐ {p.rating} · {p.category} · {p.time} away</p><button className="outline">＋ Add to Trip</button></Card>)}</div></div>}
function MapPage({trip}){return <div><PageTitle title="Optimized route" sub="Every stop is ordered to reduce travel time and transport cost."/><Card cls="map"><div className="mapBg"><div className="routeLine"/>{["Hotel","Heritage","Market","Beach","Dinner"].map((x,i)=><div className="pin" style={{left:(15+i*18)+"%",top:(55-Math.sin(i)*25)+"%"}}><span>{i+1}</span><small>{x}</small></div>)}<div className="mapLabel">GOA · AI ROUTE</div></div><div className="mapStats"><Metric icon="⏱️" title="Total travel" value="42 min" sub="24 min saved"/><Metric icon="🚕" title="Transport" value="₹380" sub="Optimized"/></div></Card><Card cls="aiNote">✨ <b>AI Route Optimization:</b> Museum → Market → Beach → Restaurant saves 24 minutes and ₹120 compared with the original order.</Card></div>}
function Itinerary({trip}){return <div><PageTitle title="Your complete itinerary" sub="A day-by-day plan generated around your preferences."/><div className="timeline">{trip.itinerary.map(d=><Card><div className="day"><span>{d.day}</span><h2>{d.title}</h2></div>{d.items.map(([time,item])=><div className="event"><b>{time}</b><div><span>{item}</span><small>AI scheduled</small></div></div>)}</Card>)}</div></div>}
function Budget({trip,whatIf}){return <div><PageTitle title="Trip Budget" sub="Your AI Budget Guardian watches every connected decision."/><div className="grid2"><Card cls="budgetBig"><span className="eyebrow">PLANNED TOTAL</span><h1>₹{trip.budget.total.toLocaleString()}</h1><div className="progress"><i style={{width:Math.min(100,trip.budget.total/trip.request.budget*100)+"%"}}/></div><p>{trip.budget.remaining>=0?"₹"+trip.budget.remaining.toLocaleString()+" remaining":"₹"+Math.abs(trip.budget.remaining).toLocaleString()+" over budget"}</p></Card><Card><div className="sectionTitle"><span>🛡️</span><div><b>Budget Guardian</b><small>Continuous optimization</small></div></div><div className="aiNote">⚠️ Your plan is monitored for price changes. If costs rise, TravelMind can search cheaper alternatives automatically.</div><button className="primary" onClick={()=>whatIf("Budget reduced to ₹18,000",18000)}>Find cheaper alternatives</button></Card></div><Card><div className="breakdown">{Object.entries(trip.budget.breakdown).map(([k,v])=><div><span>{k}</span><b>₹{v.toLocaleString()}</b></div>)}</div></Card></div>}
function Live({trip}){return <div><div className="liveHero"><div className="live"><i/> TRIP IS LIVE</div><h1>Next: Heritage Museum</h1><p>📍 14 min away · Traffic: Moderate</p><button className="primary"><Navigation size={16}/> Navigate</button></div><Card cls="alert"><span>⚠️</span><div><b>PLAN CHANGE DETECTED</b><h2>What if your next place becomes unavailable?</h2><p>TravelMind can find an alternative, recalculate the route and update the rest of your day.</p></div><button className="outline">Simulate change</button></Card><Card><div className="sectionTitle"><span>☁️</span><div><b>Live monitoring</b><small>Weather · disruptions · route conditions</small></div></div><div className="monitor"><span>☁️ 28°C</span><span>🚦 Moderate traffic</span><span>🛡️ No safety alerts</span></div></Card></div>}
function PageTitle({title,sub}){return <div className="pageTitle"><h1>{title}</h1><p>{sub}</p></div>}
createRoot(document.getElementById("root")).render(<App/>);
