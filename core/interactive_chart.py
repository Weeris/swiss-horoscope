"""
Interactive Chart Wheel using Plotly
Clickable planets with hover details
"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Optional

# Planet glyphs and colors (matching chart_wheel.py)
PLANET_GLYPHS = {
    'Sun': '☉', 'Moon': '☽', 'Mercury': '☿', 'Venus': '♀', 'Mars': '♂',
    'Jupiter': '♃', 'Saturn': '♄', 'Uranus': '⛢', 'Neptune': '♆',
    'Pluto': '♇', 'North Node': '☊', 'South Node': '☋'
}

PLANET_COLORS = {
    'Sun': '#FFD700', 'Moon': '#C0C0C0', 'Mercury': '#A9A9A9', 'Venus': '#FFA500',
    'Mars': '#FF4500', 'Jupiter': '#DAA520', 'Saturn': '#D2691E', 'Uranus': '#40E0D0',
    'Neptune': '#4169E1', 'Pluto': '#8B4513', 'North Node': '#FF69B4', 'South Node': '#FFB6C1'
}

SIGN_COLORS = {
    'Aries': '#FF6B6B', 'Taurus': '#4ECDC4', 'Gemini': '#FFE66D', 'Cancer': '#95E1D3',
    'Leo': '#F38181', 'Virgo': '#AA96DA', 'Libra': '#FCBAD3', 'Scorpio': '#A8D8EA',
    'Sagittarius': '#FF9F43', 'Capricorn': '#6C5CE7', 'Aquarius': '#74B9FF', 'Pisces': '#DFE6E9'
}

SIGN_GLYPHS = {'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
               'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
               'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'}

ELEMENTS = {
    'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
    'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
    'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
    'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
}

PLANET_DESCRIPTIONS = {
    'Sun': 'The core of your identity and life force. Represents your ego and vitality.',
    'Moon': 'Your emotional nature and inner needs. Rules your instincts and habits.',
    'Mercury': 'Your communication style, thinking pattern, and how you process information.',
    'Venus': 'Rules love, beauty, aesthetics, and what you value in life.',
    'Mars': 'Represents your energy, drive, ambition, and how you take action.',
    'Jupiter': 'Governs growth, luck, expansion, and opportunities.',
    'Saturn': 'Rules discipline, structure, responsibilities, and life lessons.',
    'Uranus': 'Rules innovation, sudden changes, uniqueness, and awakening.',
    'Neptune': 'Governs dreams, intuition, spirituality, and imagination.',
    'Pluto': 'Rules transformation, power, rebirth, and the subconscious.'
}


def normalize_angle(angle: float) -> float:
    return angle % 360


def degree_to_chart_coords(longitude: float, radius: float) -> tuple:
    """Convert zodiac longitude to chart coordinates (0° = right, counter-clockwise)"""
    angle = np.radians(90 - longitude)
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y


def create_interactive_chart_wheel(
    planets: Dict,
    houses: Dict,
    ascendant: Dict,
    midheaven: Dict,
    aspects: Optional[List[Dict]] = None,
    show_aspects: bool = True,
    show_houses: bool = True,
    width: int = 700,
    height: int = 700
) -> go.Figure:
    """Create an interactive Plotly chart wheel"""
    
    fig = go.Figure()
    
    # Set dark background
    fig.update_layout(
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#1a1a2e',
        width=width,
        height=height,
        xaxis=dict(range=[-1.3, 1.3], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-1.3, 1.3], showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest'
    )
    
    outer_radius = 1.0
    house_radius = 0.85
    planet_radius = 0.55
    
    # Draw sign segments
    for i, sign in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']):
        start_angle = 90 - i * 30
        end_angle = start_angle - 30
        
        # Convert to radians for plotly (0° at right, clockwise)
        theta1 = np.radians(start_angle)
        theta2 = np.radians(end_angle)
        
        # Draw wedge
        fig.add_shape(
            type="circle",
            x0=outer_radius - (outer_radius - house_radius),
            y0=outer_radius - (outer_radius - house_radius),
            x1=outer_radius,
            y1=outer_radius,
            layer="below",
            fillcolor=SIGN_COLORS.get(sign, '#333'),
            opacity=0.6,
            xref="x", yref="y"
        )
        
        # Sign glyph at center of each sign
        mid_angle = start_angle - 15
        glyph_x = (outer_radius - 0.05) * np.cos(np.radians(90 - mid_angle))
        glyph_y = (outer_radius - 0.05) * np.sin(np.radians(90 - mid_angle))
        
        fig.add_annotation(
            x=glyph_x, y=glyph_y,
            text=SIGN_GLYPHS.get(sign, ''),
            showarrow=False,
            font=dict(size=12, color='white'),
            xanchor='center', yanchor='center'
        )
    
    # Draw outer circle
    theta_circle = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(
        x=outer_radius * np.cos(theta_circle),
        y=outer_radius * np.sin(theta_circle),
        mode='lines',
        line=dict(color='#4a4a6a', width=2),
        hoverinfo='skip'
    ))
    
    # Draw house circle
    if show_houses:
        fig.add_trace(go.Scatter(
            x=house_radius * np.cos(theta_circle),
            y=house_radius * np.sin(theta_circle),
            mode='lines',
            line=dict(color='#3d3d5c', width=2),
            hoverinfo='skip'
        ))
        
        # House cusps
        for house_num in range(1, 13):
            if house_num in houses:
                cusp = houses[house_num]
                long = cusp['longitude']
                x1, y1 = degree_to_chart_coords(long, house_radius)
                x2, y2 = degree_to_chart_coords(long, outer_radius)
                
                fig.add_trace(go.Scatter(
                    x=[x1, x2], y=[y1, y2],
                    mode='lines',
                    line=dict(color='#4a4a6a', width=1),
                    hoverinfo='skip'
                ))
                
                # House number
                mid_long = (long + 15) % 360
                hx, hy = degree_to_chart_coords(mid_long, (house_radius + outer_radius) / 2)
                fig.add_annotation(
                    x=hx, y=hy,
                    text=str(house_num),
                    showarrow=False,
                    font=dict(size=8, color='#888'),
                    xanchor='center', yanchor='center'
                )
    
    # Draw aspect lines
    if show_aspects and aspects:
        planet_positions = {p: degree_to_chart_coords(planets[p]['longitude'], planet_radius) 
                          for p in planets if p in planets}
        
        aspect_colors = {
            'Conjunction': '#FFFFFF',
            'Opposition': '#FF6B6B',
            'Square': '#FF4500',
            'Trine': '#4ECDC4',
            'Sextile': '#95E1D3'
        }
        
        for aspect in aspects[:15]:
            p1, p2 = aspect['p1'], aspect['p2']
            if p1 in planet_positions and p2 in planet_positions:
                x1, y1 = planet_positions[p1]
                x2, y2 = planet_positions[p2]
                color = aspect_colors.get(aspect['type'], '#666')
                
                fig.add_trace(go.Scatter(
                    x=[x1, x2], y=[y1, y2],
                    mode='lines',
                    line=dict(color=color, width=1.5),
                    opacity=0.5,
                    hoverinfo='skip'
                ))
    
    # Draw planets
    for planet, data in planets.items():
        long = data['longitude']
        sign = data.get('sign', 'Unknown')
        degree = data.get('degree', 0)
        house = data.get('house', 'N/A')
        is_retrograde = data.get('retrograde', False)
        element = ELEMENTS.get(sign, 'Unknown')
        
        x, y = degree_to_chart_coords(long, planet_radius)
        
        # Get description
        description = PLANET_DESCRIPTIONS.get(planet, 'Unknown planet')
        sign_traits = {
            'Fire': 'Bold, energetic, pioneering',
            'Earth': 'Patient, reliable, practical', 
            'Air': 'Curious, adaptable, communicative',
            'Water': 'Intuitive, emotional, compassionate'
        }
        traits = sign_traits.get(element, '')
        
        # Hover text
        hover_text = f"<b>{planet}</b><br>"
        hover_text += f"Sign: {sign} ({element})<br>"
        hover_text += f"Degree: {int(degree)}°{int((degree % 1) * 60)}'<br>"
        hover_text += f"House: {house}<br>"
        hover_text += f"Retrograde: {'Yes' if is_retrograde else 'No'}<br>"
        hover_text += f"<br><i>{description}</i>"
        
        # Planet marker
        glyph = PLANET_GLYPHS.get(planet, '●')
        color = PLANET_COLORS.get(planet, '#888')
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=30, color=color, line=dict(color='white', width=2)),
            text=glyph,
            textposition='middle center',
            textfont=dict(size=14, color='black'),
            hovertemplate=hover_text + "<extra></extra>",
            name=planet
        ))
        
        # Planet name label
        name_x, name_y = degree_to_chart_coords(long, planet_radius - 0.12)
        fig.add_annotation(
            x=name_x, y=name_y,
            text=planet,
            showarrow=False,
            font=dict(size=8, color='#ccc'),
            xanchor='center', yanchor='center'
        )
    
    # ASC and MC markers
    if ascendant:
        asc_long = ascendant['longitude']
        ax, ay = degree_to_chart_coords(asc_long, house_radius - 0.08)
        fig.add_annotation(
            x=ax, y=ay,
            text="ASC",
            showarrow=False,
            font=dict(size=10, color='#00FF00', weight='bold'),
            xanchor='center', yanchor='center'
        )
    
    if midheaven:
        mc_long = midheaven['longitude']
        mx, my = degree_to_chart_coords(mc_long, house_radius - 0.08)
        fig.add_annotation(
            x=mx, y=my,
            text="MC",
            showarrow=False,
            font=dict(size=10, color='#FFD700', weight='bold'),
            xanchor='center', yanchor='center'
        )
    
    # Title
    fig.update_layout(
        title=dict(
            text="Interactive Birth Chart",
            font=dict(size=16, color='white'),
            y=0.98
        )
    )
    
    return fig
