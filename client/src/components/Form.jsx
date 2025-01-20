import React, { useState } from "react";
import axios from "axios";
import '../index.css';

const Form = () => {
  const [formData, setFormData] = useState({
    name: "",
    country: "",
    reason: "",
  });
  const [loading, setLoading] = useState(false);

  // handling audio and translation
  const handleSpeechToText = async (field) => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/speech-to-text-translate-live");
      if (response.data.translated_text) {
        setFormData({ ...formData, [field]: response.data.translated_text });
      }
    } catch (error) {
      console.error("Error during speech-to-text:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      alert("Form submitted successfully!");
      setFormData({ name: "", country: "", reason: "" });
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Failed to submit form.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 bg-cover" style={{
        backgroundImage: "url('https://static.vecteezy.com/system/resources/previews/006/484/799/non_2x/silhouette-world-map-vector.jpg')"
    }}>
      <form
        className="w-full max-w-lg bg-white p-8 rounded shadow-md"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-bold mb-6 text-gray-800">
          Immigrant Form
        </h2>

        {/* Campo Name */}
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Name</label>
          <div className="flex items-center gap-2">
            <input
              type="text"
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
              value={formData.name}
              readOnly
            />
            <button
              type="button"
              className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:ring"
              onClick={() => handleSpeechToText("name")}
            >
              🎤
            </button>
          </div>
        </div>

        {/* Campo Country */}
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Country</label>
          <div className="flex items-center gap-2">
            <input
              type="text"
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
              value={formData.country}
              readOnly
            />
            <button
              type="button"
              className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:ring"
              onClick={() => handleSpeechToText("country")}
            >
              🎤
            </button>
          </div>
        </div>

        {/* Campo Reason */}
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Reason</label>
          <div className="flex items-center gap-2">
            <textarea
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-300"
              value={formData.reason}
              readOnly
              rows={3}
            />
            <button
              type="button"
              className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:ring"
              onClick={() => handleSpeechToText("reason")}
            >
              🎤
            </button>
          </div>
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-green-500 text-white font-bold rounded hover:bg-green-600 focus:ring"
          disabled={loading}
        >
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>
    </div>
  );
};

export default Form;