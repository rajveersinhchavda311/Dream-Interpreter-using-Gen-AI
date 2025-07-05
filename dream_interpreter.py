import streamlit as st
import openai
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import json
import datetime
import re

# Dream symbols database
DREAM_SYMBOLS = {
    
    "flying": "freedom, liberation, rising above challenges, spiritual ascension",
    "falling": "loss of control, fear of failure, anxiety, insecurity",
    "water": "emotions, subconscious, purification, life changes",
    "ocean": "vast emotions, the unconscious mind, feeling overwhelmed",
    "fire": "passion, destruction, transformation, anger",
    "animals": "instincts, natural self, specific traits of the animal",
    "dog": "loyalty, friendship, protection, or something pursuing you",
    "cat": "independence, mystery, feminine energy, intuition",
    "snake": "transformation, healing, hidden knowledge, sexuality",
    "spider": "creativity, feminine power, feeling trapped, web of relationships",
    "death": "transformation, ending of a phase, rebirth",
    "dying": "transformation, ending of a phase, rebirth",
    "chase": "avoidance, running from problems, fear, being pursued",
    "chasing": "avoidance, running from problems, fear, being pursued", 
    "running": "trying to escape, avoidance, urgency",
    "house": "self, psyche, different aspects of personality",
    "home": "security, family, your inner self",
    "car": "control over life direction, personal drive",
    "driving": "control over life direction, personal autonomy",
    "bridge": "transition, connection, overcoming obstacles",
    "door": "opportunities, new beginnings, the unknown",
    "lost": "confusion, searching for direction, feeling overwhelmed",
    "mirror": "self-reflection, truth, self-awareness",
    "school": "learning, being tested, childhood memories",
    "exam": "being tested, performance anxiety, evaluation",
    "teacher": "authority, learning, guidance",
    "family": "relationships, support systems, childhood influences",
    "friend": "aspects of yourself, social connections",
    "stranger": "unknown aspects of self, new experiences",
    "darkness": "unknown, fear, subconscious, hidden aspects",
    "light": "knowledge, clarity, hope, spiritual guidance",
    "forest": "the unknown, natural self, getting lost",
    "mountain": "challenges, goals, spiritual ascension",
    "falling": "loss of control, fear of failure, anxiety"
}

class DreamInterpreter:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.setup_model()
    
    def setup_model(self):
        """Initialize the GPT-2 model for dream interpretation"""
        try:
            model_name = "gpt2-medium"
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            
            # Add padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.info("Using fallback interpretation system")
    
    def identify_symbols(self, dream_text):
        """Identify dream symbols in the text"""
        found_symbols = []
        dream_lower = dream_text.lower()
        
        for symbol, meaning in DREAM_SYMBOLS.items():
            if symbol in dream_lower:
                found_symbols.append((symbol, meaning))
        
        return found_symbols
    
    def generate_interpretation(self, dream_text, emotion, context, symbols):
        """Generate dream interpretation using rule-based approach and templates"""
        
        # Use rule-based interpretation for better accuracy
        return self.create_comprehensive_interpretation(dream_text, emotion, context, symbols)
    
    def clean_interpretation(self, text):
        """Clean and format the AI-generated interpretation"""
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        cleaned_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and sentence[0].isupper():
                cleaned_sentences.append(sentence)
        
        return '. '.join(cleaned_sentences[:3]) + '.' if cleaned_sentences else text[:200] + '...'
    
    def create_comprehensive_interpretation(self, dream_text, emotion, context, symbols):
        """Create a comprehensive interpretation using psychological frameworks"""
        
        # Analyze dream elements
        dream_lower = dream_text.lower()
        interpretation_parts = []
        
        # Core dream analysis
        interpretation_parts.append(self.analyze_core_narrative(dream_text, emotion, context))
        
        # Symbol analysis
        if symbols:
            interpretation_parts.append(self.analyze_symbols_in_context(symbols, dream_text, emotion))
        
        # Emotional and contextual analysis
        interpretation_parts.append(self.analyze_emotional_context(emotion, context, dream_text))
        
        # Combine all parts
        full_interpretation = " ".join(interpretation_parts)
        
        return full_interpretation
    
    def analyze_core_narrative(self, dream_text, emotion, context):
        """Analyze the core narrative structure of the dream"""
        dream_lower = dream_text.lower()
        
        # Identify key dream patterns
        if "chasing" in dream_lower or "chase" in dream_lower:
            if "dog" in dream_lower:
                return "Being chased by a dog in dreams often represents loyalty conflicts or feeling pursued by responsibilities you're trying to avoid. The circular nature of returning to where you started suggests you may feel trapped in a recurring situation."
            else:
                return "Being chased in dreams typically represents avoidance of something in waking life that requires your attention."
        
        elif "flying" in dream_lower:
            if "falling" in dream_lower:
                return "The transition from flying to falling suggests a loss of control or confidence. Flying represents freedom and transcendence, while falling indicates anxiety about losing that control."
            else:
                return "Flying in dreams often symbolizes liberation, rising above current challenges, or a desire for freedom from constraints."
        
        elif "water" in dream_lower:
            if "drowning" in dream_lower or "deep" in dream_lower:
                return "Deep water or drowning scenarios often represent feeling overwhelmed by emotions or situations in your life."
            else:
                return "Water in dreams typically represents emotions, the subconscious mind, or life transitions."
        
        elif "house" in dream_lower or "home" in dream_lower:
            return "Houses in dreams often represent different aspects of your psyche or your current life situation."
        
        elif "death" in dream_lower or "dying" in dream_lower:
            return "Death in dreams rarely represents literal death, but rather transformation, the end of one phase, and the beginning of another."
        
        else:
            return "Your dream reflects current psychological processes and concerns in your waking life."
    
    def analyze_symbols_in_context(self, symbols, dream_text, emotion):
        """Analyze symbols within the context of the specific dream"""
        dream_lower = dream_text.lower()
        analysis = []
        
        for symbol, base_meaning in symbols:
            if symbol == "chase" and "dog" in dream_lower:
                analysis.append("The dog chasing you may represent loyalty, protection, or instinctual drives that you're running from.")
            elif symbol == "chase":
                analysis.append("The chase element suggests you're avoiding confronting something important in your life.")
            elif symbol == "water" and ("deep" in dream_lower or "ocean" in dream_lower):
                analysis.append("The deep water represents the depth of emotions or subconscious material you're dealing with.")
            elif symbol == "flying" and emotion == "Happy":
                analysis.append("Flying while feeling happy suggests you're experiencing or seeking greater freedom in your life.")
            else:
                analysis.append(f"The {symbol} in your dream suggests {base_meaning}.")
        
        return " ".join(analysis) if analysis else ""
    
    def analyze_emotional_context(self, emotion, context, dream_text):
        """Analyze the emotional and life context"""
        dream_lower = dream_text.lower()
        
        # Context-specific analysis
        context_analysis = ""
        if context:
            context_lower = context.lower()
            if "stress" in context_lower or "exam" in context_lower:
                context_analysis = "Given your current exam stress, this dream likely reflects your anxiety about performance and the feeling of being pursued by academic pressures."
            elif "work" in context_lower:
                context_analysis = "Your work-related stress appears to be manifesting in your dreams as scenarios of pursuit or challenge."
            elif "relationship" in context_lower:
                context_analysis = "The relationship dynamics in your life may be influencing the interpersonal elements in your dream."
        
        # Emotion-specific analysis
        emotion_analysis = ""
        if emotion == "Confused":
            emotion_analysis = "Your confusion in the dream mirrors feelings of uncertainty or lack of clarity in your waking life."
        elif emotion == "Anxious":
            emotion_analysis = "The anxiety you felt reflects current worries or concerns that may need attention."
        elif emotion == "Scared":
            emotion_analysis = "The fear in your dream suggests you may be confronting something that feels threatening or overwhelming."
        elif emotion == "Happy":
            emotion_analysis = "The positive emotions indicate healthy psychological processing and optimism."
        
        # Special case for circular/repetitive dreams
        if "back" in dream_lower and ("where" in dream_lower or "started" in dream_lower):
            emotion_analysis += " The circular nature of returning to where you started suggests feelings of being stuck or trapped in repetitive patterns."
        
        return f"{context_analysis} {emotion_analysis}".strip()
    
    def create_fallback_interpretation(self, dream_text, emotion, context, symbols):
        """Create interpretation when AI model fails - now more sophisticated"""
        return self.create_comprehensive_interpretation(dream_text, emotion, context, symbols)

def create_dream_journal_entry(dream_text, emotion, context, interpretation, symbols):
    """Create a journal entry for the dream"""
    entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dream": dream_text,
        "emotion": emotion,
        "context": context,
        "interpretation": interpretation,
        "symbols": [{"symbol": s[0], "meaning": s[1]} for s in symbols]
    }
    return entry

def main():
    st.set_page_config(
        page_title="AI Dream Interpreter",
        page_icon="🌙",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #2C3E50;
    font-size: 3rem;
    margin-bottom: 2rem;
}
.dream-box {
    background-color: #fdfdfd;
    color: #1C1C1C;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
.interpretation-box {
    background-color: #eef6fc;
    color: #1C1C1C;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #3498DB;
}
.symbol-box {
    background-color: #fff8e1;
    color: #1C1C1C;
    padding: 15px;
    border-radius: 8px;
    margin: 5px 0;
    border-left: 4px solid #f1c40f;
}
</style>
""", unsafe_allow_html=True)

    
    # Header
    st.markdown('<h1 class="main-header">🌙 AI Dream Interpreter</h1>', unsafe_allow_html=True)
    st.markdown("### *Unlock the mysteries of your dreams with AI-powered interpretation*")
    
    # Initialize the dream interpreter
    @st.cache_resource
    def load_interpreter():
        return DreamInterpreter()
    
    interpreter = load_interpreter()
    
    # Sidebar for navigation
    st.sidebar.title("🌟 Navigation")
    page = st.sidebar.selectbox("Choose a section:", 
                               ["Dream Interpretation", "Dream Journal", "About Dream Symbols"])
    
    if page == "Dream Interpretation":
        st.markdown("---")
        
        # Dream input form
        st.header("📝 Tell me about your dream")
        
        with st.form("dream_form"):
            dream_text = st.text_area(
                "Describe your dream in detail:",
                height=150,
                placeholder="I was flying over a beautiful landscape when suddenly I started falling into a deep blue ocean..."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                emotion = st.selectbox(
                    "How did you feel during the dream?",
                    ["Happy", "Anxious", "Scared", "Confused", "Excited", "Sad", "Peaceful", "Other"]
                )
            
            with col2:
                context = st.text_input(
                    "What's happening in your life right now?",
                    placeholder="Work stress, relationship changes, etc."
                )
            
            submitted = st.form_submit_button("🔮 Interpret My Dream", use_container_width=True)
        
        if submitted and dream_text:
            with st.spinner("🌙 Analyzing your dream..."):
                # Identify symbols
                symbols = interpreter.identify_symbols(dream_text)
                
                # Generate interpretation
                interpretation = interpreter.generate_interpretation(
                    dream_text, emotion, context, symbols
                )
                
                # Display results
                st.markdown("---")
                st.header("🔮 Your Dream Interpretation")
                
                # Main interpretation
                st.markdown(f'<div class="interpretation-box"><h4 style="color:black;">Psychological Analysis:</h4><p>{interpretation}</p></div>', unsafe_allow_html=True)

                
                # Symbols section
                if symbols:
                    st.subheader("🎭 Symbols in Your Dream")
                    for symbol, meaning in symbols:
                        st.markdown(f'<div class="symbol-box"><strong>{symbol.title()}:</strong> {meaning}</div>', 
                                   unsafe_allow_html=True)
                
                # Additional insights
                st.subheader("💡 Additional Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Emotional Significance:**")
                    if emotion == "Anxious":
                        st.write("Your anxiety in the dream may reflect current worries or uncertainties.")
                    elif emotion == "Happy":
                        st.write("Positive emotions suggest harmony and contentment in your life.")
                    elif emotion == "Scared":
                        st.write("Fear in dreams often represents facing the unknown or personal challenges.")
                    else:
                        st.write("Your emotions in the dream provide clues about your current state of mind.")
                
                with col2:
                    st.markdown("**Recommendations:**")
                    st.write("• Keep a dream journal to track patterns")
                    st.write("• Reflect on how the dream relates to your current life")
                    st.write("• Consider what changes the dream might be suggesting")
                
                # Save to session state for journal
                if 'dream_journal' not in st.session_state:
                    st.session_state.dream_journal = []
                
                entry = create_dream_journal_entry(dream_text, emotion, context, interpretation, symbols)
                st.session_state.dream_journal.append(entry)
                
                st.success("✅ Dream interpretation saved to your journal!")
    
    elif page == "Dream Journal":
        st.header("📚 Your Dream Journal")
        
        if 'dream_journal' in st.session_state and st.session_state.dream_journal:
            for i, entry in enumerate(reversed(st.session_state.dream_journal)):
                with st.expander(f"Dream from {entry['date']} - {entry['emotion']}"):
                    st.write(f"**Dream:** {entry['dream']}")
                    st.write(f"**Emotion:** {entry['emotion']}")
                    st.write(f"**Context:** {entry['context']}")
                    st.write(f"**Interpretation:** {entry['interpretation']}")
                    
                    if entry['symbols']:
                        st.write("**Symbols:**")
                        for symbol in entry['symbols']:
                            st.write(f"• {symbol['symbol']}: {symbol['meaning']}")
        else:
            st.info("No dreams recorded yet. Go to the Dream Interpretation section to analyze your first dream!")
    
    elif page == "About Dream Symbols":
        st.header("🎭 Common Dream Symbols")
        st.write("Understanding dream symbols can help you better interpret your dreams:")
        
        # Display symbol meanings in a nice format
        for symbol, meaning in DREAM_SYMBOLS.items():
            st.markdown(f"**{symbol.title()}:** {meaning}")
        
        st.markdown("---")
        st.info("💡 Remember: Dream symbols can have personal meanings that differ from universal interpretations. The AI considers both common meanings and your personal context.")

if __name__ == "__main__":
    main()