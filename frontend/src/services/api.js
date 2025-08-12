const API_BASE_URL = 'http://localhost:5000/api';

// Helper function to make API calls
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong');
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Authentication APIs
export const authAPI = {
  register: async (userData) => {
    return apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  login: async (credentials) => {
    return apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },
};

// Complaint APIs
export const complaintAPI = {
  fileComplaint: async (complaintData) => {
    return apiCall('/complaint/file', {
      method: 'POST',
      body: JSON.stringify(complaintData),
    });
  },

  getComplaintStatus: async (userId) => {
    return apiCall(`/complaint/status?userId=${userId}`, {
      method: 'GET',
    });
  },

  resolveComplaint: async (complaintId) => {
    return apiCall('/complaint/resolve', {
      method: 'POST',
      body: JSON.stringify({ complaintId }),
    });
  },

  submitFeedback: async (feedbackData) => {
    return apiCall('/complaint/feedback', {
      method: 'POST',
      body: JSON.stringify(feedbackData),
    });
  },
};

// Schemes APIs
export const schemesAPI = {
  findSchemes: async (userData) => {
    return apiCall('/schemes/find', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
};

// Helpline APIs
export const helplineAPI = {
  getHelplineNumbers: async (state) => {
    return apiCall(`/helpline?state=${encodeURIComponent(state)}`, {
      method: 'GET',
    });
  },
};

// Voice Processing APIs
export const voiceAPI = {
  detectLanguage: async (text) => {
    return apiCall('/voice/detect-language', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  },

  voiceToText: async (voiceData) => {
    return apiCall('/voice/voice-to-text', {
      method: 'POST',
      body: JSON.stringify(voiceData),
    });
  },

  analyzeWithGemini: async (voiceData) => {
    return apiCall('/voice/analyze-with-gemini', {
      method: 'POST',
      body: JSON.stringify(voiceData),
    });
  },

  getLanguageSupport: async () => {
    return apiCall('/voice/get-language-support', {
      method: 'GET',
    });
  },
};

// AI Simulation APIs (placeholder functions)
export const aiAPI = {
  // Fallback transcription for when Web Speech API is not available
  transcribeAudio: async (audioBlob) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simulate transcription result
    return {
      text: "This is a simulated transcription result.",
      confidence: 0.85
    };
  },

  // Analyze problem description and suggest helpline categories
  analyzeProblem: async (problemData) => {
    return apiCall('/ai/analyze-problem', {
      method: 'POST',
      body: JSON.stringify(problemData),
    });
  },

  // AI-powered scheme recommendation based on problem analysis
  recommendSchemes: async (problemData) => {
    return apiCall('/ai/recommend-schemes', {
      method: 'POST',
      body: JSON.stringify(problemData),
    });
  },

  // Simulate CLIP/SAM API for image analysis
  analyzeImage: async (imageFile) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Return dummy analysis
    const dummyAnalyses = [
      "Image shows garbage overflow in residential area",
      "Image shows water leak from pipeline",
      "Image shows broken street light",
      "Image shows potholes on road",
      "Image shows sewage overflow"
    ];
    
    return {
      description: dummyAnalyses[Math.floor(Math.random() * dummyAnalyses.length)],
      confidence: 0.85 + Math.random() * 0.1
    };
  },

  // Generate complaint draft using Gemini AI
  generateComplaintDraft: async (inputs) => {
    const { userInfo, address, issueDescription, category, region } = inputs;
    
    try {
      // Call backend API to generate draft using Gemini AI
      const response = await apiCall('/complaint/generate-draft', {
        method: 'POST',
        body: JSON.stringify({
          userInfo,
          address,
          issueDescription,
          category,
          region
        }),
      });
      
      // Check if the response contains an error message
      if (response.draft && response.draft.startsWith('Error generating complaint draft:')) {
        console.warn('AI generation failed, using fallback template');
        throw new Error('AI generation failed');
      }
      
      return response;
    } catch (error) {
      console.error('Failed to generate AI draft:', error);
      // Fallback to dynamic template if AI generation fails
      const subjectVariations = [
        `Complaint regarding ${category} issue in ${region}`,
        `Urgent: ${category} problem in ${region}`,
        `Request for immediate action on ${category} issue`,
        `Complaint about ${category} services in ${region}`,
        `Report of ${category} issue requiring attention`
      ];
      
      const openingVariations = [
        `Dear ${category} Department,`,
        `To the ${category} Department,`,
        `Respected ${category} Department,`,
        `Dear Sir/Madam of ${category} Department,`,
        `To Whom It May Concern,`
      ];
      
      const urgencyVariations = [
        "requires immediate attention",
        "needs urgent intervention", 
        "demands prompt action",
        "calls for immediate resolution",
        "requires your immediate attention"
      ];
      
      const impactVariations = [
        "This issue is affecting the daily lives of residents in our area and requires prompt action from your department.",
        "The situation is causing significant inconvenience to the local community and needs immediate resolution.",
        "This problem is impacting the quality of life for residents and requires urgent attention.",
        "The issue is creating difficulties for the neighborhood and needs prompt intervention.",
        "This matter is affecting public welfare and requires immediate action from your department."
      ];
      
      const closingVariations = [
        "I kindly request you to investigate this matter and take necessary steps to resolve it at the earliest.",
        "I would appreciate if you could look into this issue and take appropriate action as soon as possible.",
        "Please consider this matter urgent and take the necessary steps to address it promptly.",
        "I hope you will give this issue the attention it deserves and resolve it quickly.",
        "I trust you will investigate this matter thoroughly and implement a solution without delay."
      ];
      
      const thankYouVariations = [
        "Thank you for your attention to this issue.",
        "I appreciate your time and consideration in this matter.",
        "Thank you for taking the time to address this concern.",
        "I look forward to your response and action on this matter.",
        "Thank you for your cooperation in resolving this issue."
      ];
      
      const signOffVariations = [
        "Best regards,",
        "Sincerely,",
        "Yours faithfully,",
        "Respectfully yours,",
        "Thank you,"
      ];
      
      // Randomly select variations
      const subject = subjectVariations[Math.floor(Math.random() * subjectVariations.length)];
      const opening = openingVariations[Math.floor(Math.random() * openingVariations.length)];
      const urgency = urgencyVariations[Math.floor(Math.random() * urgencyVariations.length)];
      const impact = impactVariations[Math.floor(Math.random() * impactVariations.length)];
      const closing = closingVariations[Math.floor(Math.random() * closingVariations.length)];
      const thankYou = thankYouVariations[Math.floor(Math.random() * thankYouVariations.length)];
      const signOff = signOffVariations[Math.floor(Math.random() * signOffVariations.length)];
      
      // Generate different body content based on category
      let bodyContent = "";
      if (category.toLowerCase().includes('water') || category.toLowerCase().includes('sanitation') || category.toLowerCase().includes('sewage')) {
        bodyContent = `I am writing to bring to your attention a ${category.toLowerCase()} issue that ${urgency} in our area.\n\n`;
      } else if (category.toLowerCase().includes('electricity') || category.toLowerCase().includes('power')) {
        bodyContent = `I am writing to report a ${category.toLowerCase()} problem that ${urgency} in our locality.\n\n`;
      } else if (category.toLowerCase().includes('roads') || category.toLowerCase().includes('transport')) {
        bodyContent = `I am writing to bring to your notice a ${category.toLowerCase()} issue that ${urgency} in our area.\n\n`;
      } else if (category.toLowerCase().includes('garbage') || category.toLowerCase().includes('waste')) {
        bodyContent = `I am writing to report a ${category.toLowerCase()} management issue that ${urgency} in our neighborhood.\n\n`;
      } else {
        bodyContent = `I am writing to bring to your attention a ${category.toLowerCase()} issue that ${urgency} in our area.\n\n`;
      }
      
      const draft = `Subject: ${subject}

${opening}

${bodyContent}Issue Details:
- Category: ${category}
- Description: ${issueDescription}
- Location: ${address.houseNo}, ${address.addressLine1}, ${address.addressLine2}, PIN: ${address.pinCode}
- Region: ${region}

Personal Information:
- Name: ${userInfo.fullName}
- Contact: ${userInfo.mobile}
- Email: ${userInfo.email}

${impact} ${closing}

${thankYou}

${signOff}
${userInfo.fullName}
${userInfo.mobile}`;

      return {
        draft,
        authority: {
          name: `${category} Department - Municipal Corporation`,
          email: `${category.toLowerCase().replace(' ', '.')}@examplecity.gov.in`,
          phone: `+91-22-${Math.floor(Math.random() * 90000000) + 10000000}`
        }
      };
    }
  }
}; 