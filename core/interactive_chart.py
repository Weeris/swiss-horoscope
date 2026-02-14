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
    
    # Draw sign segments as wedges using shapes
    for i, sign in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']):
        start_angle = 90 - i * 30
        end_angle = start_angle - 30
        
        # Draw wedge using shapes (pie slices)
        fig.add_shape(
            type="path",
            path=f"M 0 0 L {outer_radius*np.cos(np.radians(start_angle))} {outer_radius*np.sin(np.radians(start_angle))} A {outer_radius} {outer_radius} 0 0 0 {outer_radius*np.cos(np.radians(end_angle))} {outer_radius*np.sin(np.radians(end_angle))} Z",
            fillcolor=SIGN_COLORS.get(sign, '#333'),
            opacity=0.5,
            line=dict(color='#2d2d44', width=1),
            layer="below"
        )
        
        # Sign glyph at center of each sign using scatter
        mid_angle = start_angle - 15
        glyph_x = (outer_radius - 0.05) * np.cos(np.radians(90 - mid_angle))
        glyph_y = (outer_radius - 0.05) * np.sin(np.radians(90 - mid_angle))
        
        fig.add_trace(go.Scatter(
            x=[glyph_x], y=[glyph_y],
            mode='text',
            text=[SIGN_GLYPHS.get(sign, '')],
            textfont=dict(size=14, color='white'),
            hoverinfo='skip'
        ))
    
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
        
        # House cusps and numbers
        house_xs, house_ys = [], []
        house_labels_x, house_labels_y, house_labels_text = [], [], []
        
        for house_num in range(1, 13):
            if house_num in houses:
                cusp = houses[house_num]
                long = cusp['longitude']
                x1, y1 = degree_to_chart_coords(long, house_radius)
                x2, y2 = degree_to_chart_coords(long, outer_radius)
                
                house_xs.extend([x1, x2, None])
                house_ys.extend([y1, y2, None])
                
                # House number position
                mid_long = (long + 15) % 360
                hx, hy = degree_to_chart_coords(mid_long, (house_radius + outer_radius) / 2)
                house_labels_x.append(hx)
                house_labels_y.append(hy)
                house_labels_text.append(str(house_num))
        
        # Draw house lines
        if house_xs:
            fig.add_trace(go.Scatter(
                x=house_xs, y=house_ys,
                mode='lines',
                line=dict(color='#4a4a6a', width=1),
                hoverinfo='skip'
            ))
        
        # Draw house numbers
        if house_labels_x:
            fig.add_trace(go.Scatter(
                x=house_labels_x, y=house_labels_y,
                mode='text',
                text=house_labels_text,
                textfont=dict(size=9, color='#888'),
                hoverinfo='skip'
            ))
    
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
        
        aspect_xs, aspect_ys = [], []
        
        for aspect in aspects[:15]:
            p1, p2 = aspect['p1'], aspect['p2']
            if p1 in planet_positions and p2 in planet_positions:
                x1, y1 = planet_positions[p1]
                x2, y2 = planet_positions[p2]
                
                aspect_xs.extend([x1, x2, None])
                aspect_ys.extend([y1, y2, None])
        
        if aspect_xs:
            fig.add_trace(go.Scatter(
                x=aspect_xs, y=aspect_ys,
                mode='lines',
                line=dict(color='#666', width=1),
                opacity=0.4,
                hoverinfo='skip'
            ))
    
    # Draw planets
    planet_xs, planet_ys = [], []
    planet_glyphs, planet_colors = [], []
    planet_hover, planet_texts = [], []
    
    for planet, data in planets.items():
        long = data['longitude']
        sign = data.get('sign', 'Unknown')
        degree = data.get('degree', 0)
        house = data.get('house', 'N/A')
        is_retrograde = data.get('retrograde', False)
        element = ELEMENTS.get(sign, 'Unknown')
        
        x, y = degree_to_chart_coords(long, planet_radius)
        
        planet_xs.append(x)
        planet_ys.append(y)
        planet_glyphs.append(PLANET_GLYPHS.get(planet, '●'))
        planet_colors.append(PLANET_COLORS.get(planet, '#888'))
        
        # Hover text
        description = PLANET_DESCRIPTIONS.get(planet, 'Unknown planet')
        hover_text = f"<b>{planet}</b><br>"
        hover_text += f"Sign: {sign} ({element})<br>"
        hover_text += f"Degree: {int(degree)}°{int((degree % 1) * 60)}'<br>"
        hover_text += f"House: {house}<br>"
        hover_text += f"Retrograde: {'Yes' if is_retrograde else 'No'}<br>"
        hover_text += f"<br><i>{description}</i>"
        planet_hover.append(hover_text)
        planet_texts.append(planet)
    
    # Draw planets as markers with glyphs
    if planet_xs:
        # Planet circles
        fig.add_trace(go.Scatter(
            x=planet_xs, y=planet_ys,
            mode='markers',
            marker=dict(
                size=28,
                color=planet_colors,
                line=dict(color='white', width=2)
            ),
            hovertemplate='%{customdata}<extra></extra>',
            customdata=planet_hover,
            name='Planets'
        ))
        
        # Planet glyphs
        fig.add_trace(go.Scatter(
            x=planet_xs, y=planet_ys,
            mode='text',
            text=planet_glyphs,
            textposition='middle center',
            textfont=dict(size=14, color='black'),
            hoverinfo='skip'
        ))
        
        # Planet names
        name_positions = []
        for planet, data in planets.items():
            long = data['longitude']
            nx, ny = degree_to_chart_coords(long, planet_radius - 0.12)
            name_positions.append((nx, ny, planet))
        
        if name_positions:
            fig.add_trace(go.Scatter(
                x=[p[0] for p in name_positions],
                y=[p[1] for p in name_positions],
                mode='text',
                text=[p[2] for p in name_positions],
                textfont=dict(size=8, color='#aaa'),
                hoverinfo='skip'
            ))
    
    # ASC and MC markers using scatter
    if ascendant:
        asc_long = ascendant['longitude']
        ax, ay = degree_to_chart_coords(asc_long, house_radius - 0.1)
        fig.add_trace(go.Scatter(
            x=[ax], y=[ay],
            mode='text',
            text=['ASC'],
            textfont=dict(size=10, color='#00FF00'),
            hoverinfo='skip'
        ))
    
    if midheaven:
        mc_long = midheaven['longitude']
        mx, my = degree_to_chart_coords(mc_long, house_radius - 0.1)
        fig.add_trace(go.Scatter(
            x=[mx], y=[my],
            mode='text',
            text=['MC'],
            textfont=dict(size=10, color='#FFD700'),
            hoverinfo='skip'
        ))
    
    # Title
    fig.update_layout(
        title=dict(
            text="Interactive Birth Chart",
            font=dict(size=16, color='white'),
            y=0.98
        )
    )
    
    return fig
