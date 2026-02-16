import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Gap {
  type: string;
  item: string;
  severity: string;
  context: string;
  suggestion: string;
}

export interface RiskFactor {
  factor: string;
  severity: string;
  details: string[];
  impact: string;
}

export interface RejectionRisk {
  level: string;
  factors: RiskFactor[];
  summary: string;
}

export interface Recommendation {
  priority: number;
  severity: string;
  action: string;
  reason: string;
  item: string;
  impact: string;
}

export interface AnalyzeResponse {
  overall_score: number;
  technical_score: number;
  personality_score: number;
  detected_domain: string;
  missing_skills: string[];
  suggestions: string[];
  traits: Record<string, number>;
  section_scores: Record<string, number>;
  error?: string;
  design_style: string;

  // New dynamic analysis fields
  gaps: Gap[];
  rejection_risk: RejectionRisk;
  recommendations: Recommendation[];
  jd_priorities: any;
}

export interface TailorResponse {
  tailored_summary: string;
  missing_keywords: string[];
  tailored_text: string;
  design_style: string;
}

export const analyzeResume = async (resumeText: string, jdText: string): Promise<AnalyzeResponse> => {
  const response = await axios.post(`${API_URL}/analyze`, {
    resume_text: resumeText,
    jd_text: jdText,
  });
  return response.data;
};

export const tailorResume = async (resumeText: string, jdText: string, designStyle: string = "modern"): Promise<TailorResponse> => {
  const response = await axios.post(`${API_URL}/tailor`, {
    resume_text: resumeText,
    jd_text: jdText,
    design_style: designStyle,
  });
  return response.data;
};

export const downloadPDF = async (data: TailorResponse) => {
  const response = await axios.post(`${API_URL}/download-pdf`, data, {
    responseType: 'blob', // Important for binary files
  });

  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'tailored_resume.pdf');
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url); // Clean up memory
};
