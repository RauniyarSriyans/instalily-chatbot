import axios from 'axios';

export const getAIMessage = async (chatlog) => {
  try {
    const response = await axios.post(`http://localhost:8000/chatbot`, {
      messages: chatlog,
    });
    return response.data;
  } catch (err) {
    console.error('error while fetching message', err);
  }
};
