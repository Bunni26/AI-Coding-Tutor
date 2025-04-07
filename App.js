import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('python');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add a test connection on component mount
  useEffect(() => {
    const testBackendConnection = async () => {
      try {
        console.log('Testing backend connection...');
        const response = await axios.post(`${API_URL}/chat`, {
          message: "test connection",
          context: []
        });
        console.log('Backend connection successful:', response.data);
      } catch (error) {
        console.error('Backend connection failed:', error);
        setError('Cannot connect to backend server. Please make sure it is running.');
      }
    };

    testBackendConnection();
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setLoading(true);
    setError(null);

    // Add user message to chat immediately
    const userMessageObj = { type: 'user', content: userMessage };
    setMessages(prev => [...prev, userMessageObj]);

    try {
      console.log('Attempting to send message to backend...');
      console.log('URL:', `${API_URL}/chat`);
      console.log('Payload:', { message: userMessage, context: messages });
      
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage,
        context: messages
      });

      console.log('Raw backend response:', response);
      console.log('Response data:', response.data);

      if (!response.data) {
        throw new Error('No response data received from server');
      }

      if (response.data.error) {
        throw new Error(response.data.error);
      }

      if (!response.data.response) {
        throw new Error('Empty response from server');
      }

      // Add AI response to chat
      const aiMessageObj = { type: 'ai', content: response.data.response };
      console.log('Adding AI response to chat:', aiMessageObj);
      setMessages(prev => [...prev, aiMessageObj]);
      
    } catch (error) {
      console.error('Error details:', {
        message: error.message,
        response: error.response,
        stack: error.stack
      });
      
      const errorMessage = error.response?.data?.error || error.message || 'Unknown error occurred';
      console.log('Setting error message:', errorMessage);
      
      setError(errorMessage);
      setMessages(prev => [...prev, {
        type: 'error',
        content: `Error: ${errorMessage}`
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', py: 4 }}>
      <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h5" component="h1">
            AI Coding Tutor
          </Typography>
          <FormControl size="small" sx={{ mt: 1 }}>
            <InputLabel id="language-select-label">Programming Language</InputLabel>
            <Select
              labelId="language-select-label"
              id="language-select"
              name="language-select"
              value={language}
              label="Programming Language"
              onChange={(e) => setLanguage(e.target.value)}
              inputProps={{
                'aria-label': 'Select programming language'
              }}
            >
              <MenuItem value="python">Python</MenuItem>
              <MenuItem value="javascript">JavaScript</MenuItem>
              <MenuItem value="java">Java</MenuItem>
              <MenuItem value="cpp">C++</MenuItem>
            </Select>
          </FormControl>
          {error && (
            <Alert 
              severity="error" 
              sx={{ mt: 1 }} 
              onClose={() => setError(null)}
            >
              {error}
            </Alert>
          )}
          {loading && (
            <Alert 
              severity="info" 
              sx={{ mt: 1 }}
            >
              Processing your request...
            </Alert>
          )}
        </Box>

        <Box sx={{ flex: 1, overflow: 'auto', p: 2, bgcolor: '#f5f5f5' }}>
          {messages.length === 0 ? (
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100%',
              color: 'text.secondary'
            }}>
              <Typography variant="body1">
                Ask me anything about programming! I'm here to help.
              </Typography>
            </Box>
          ) : (
            messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  mb: 2,
                  display: 'flex',
                  flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '80%',
                    backgroundColor: message.type === 'user' ? 'primary.light' : 
                                   message.type === 'error' ? '#ffebee' : '#ffffff',
                    color: message.type === 'user' ? 'primary.contrastText' : 
                           message.type === 'error' ? '#c62828' : 'text.primary',
                  }}
                >
                  {message.type === 'user' ? (
                    <Typography>{message.content}</Typography>
                  ) : (
                    <ReactMarkdown
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={vscDarkPlus}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        },
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  )}
                </Paper>
              </Box>
            ))
          )}
          <div ref={messagesEndRef} />
        </Box>

        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider', bgcolor: '#ffffff' }}>
          <Box 
            component="form" 
            sx={{ display: 'flex', gap: 1 }}
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
          >
            <FormControl fullWidth>
              <TextField
                id="chat-input"
                name="chat-input"
                label="Ask a coding question"
                aria-label="Chat input"
                fullWidth
                multiline
                maxRows={4}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder=""
                variant="outlined"
                disabled={loading}
                sx={{ bgcolor: '#ffffff' }}
              />
            </FormControl>
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !input.trim()}
              aria-label="Send message"
              endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default App; 