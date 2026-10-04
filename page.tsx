'use client';
import { useEffect, useState } from 'react';

// Abhi ke liye testing user ID. Jab Auth lagaoge tab ise dynamic kar dena.
const TEST_USER_ID = "00000000-0000-0000-0000-000000000000"; // Supabase me ek test user banakar uski ID yahan dalna

export default function Home() {
  const [matches, setMatches] = useState<any[]>([]);
  const [roomDetails, setRoomDetails] = useState<{ [key: string]: any }>({});
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      const res = await fetch(`${API_URL}/api/matches/list`);
      const data = await res.json();
      setMatches(data);
    } catch (error) {
      console.error("Matches fetch nahi hue:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async (matchId: string) => {
    try {
      const res = await fetch(`${API_URL}/api/matches/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: TEST_USER_ID, match_id: matchId })
      });
      const data = await res.json();
      
      if (data.success) {
        alert("Match Joined Successfully! Ab aap ID/Pass dekh sakte ho.");
      } else {
        alert(data.detail || "Join fail ho gaya.");
      }
    } catch (error) {
      alert("Error joining match.");
    }
  };

  const viewRoomDetails = async (matchId: string) => {
    try {
      const res = await fetch(`${API_URL}/api/matches/${matchId}/room-details?user_id=${TEST_USER_ID}`);
      const data = await res.json();
      
      if (data.success) {
        setRoomDetails(prev => ({ ...prev, [matchId]: data.data }));
      } else {
        alert(data.error);
      }
    } catch (error) {
      alert("ID/Pass fetch nahi ho paya.");
    }
  };

  if (loading) return <div className="text-center mt-20 text-white">Loading Matches...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold text-orange-500 mb-8 text-center">Free Fire Custom Tournaments</h1>
      
      <div className="max-w-3xl mx-auto space-y-6">
        {matches.map((match) => (
          <div key={match.id} className="bg-gray-800 p-6 rounded-lg border border-gray-700 shadow-lg">
            <h2 className="text-xl font-bold mb-2">{match.title}</h2>
            <p className="text-gray-400 mb-4">Time: {new Date(match.match_time).toLocaleString()}</p>
            
            <div className="flex space-x-4 mb-4">
              <button 
                onClick={() => handleJoin(match.id)}
                className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded font-semibold transition"
              >
                Join Match
              </button>
              <button 
                onClick={() => viewRoomDetails(match.id)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-semibold transition"
              >
                View ID / Pass
              </button>
            </div>

            {/* Room Details Box */}
            {roomDetails[match.id] && (
              <div className="bg-gray-900 p-4 rounded mt-4 border border-orange-500">
                <p className="text-green-400 font-mono">
                  Room ID: {roomDetails[match.id].room_id || "Abhi update nahi hua"}
                </p>
                <p className="text-red-400 font-mono">
                  Password: {roomDetails[match.id].room_password || "Abhi update nahi hua"}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}