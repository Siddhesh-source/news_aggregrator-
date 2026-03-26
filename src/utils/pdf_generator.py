import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from html import escape
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text(text):
    """Clean text for PDF rendering - remove emojis and special characters."""
    if not text:
        return ""
    # Remove emojis and other problematic Unicode characters
    cleaned = ''.join(char for char in text if ord(char) < 0x10000)
    return escape(cleaned)


def generate_pdf_analysis(articles, filename="upsc_daily_analysis.pdf"):
    """
    Generate a detailed PDF analysis tailored for UPSC exam preparation.
    Premium newsletter design with seamless flow.
    
    Args:
        articles: List of article dicts with analysis
        filename: Output PDF filename
        
    Returns:
        str: Path to generated PDF
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.5*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles with premium newsletter design
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.white,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=42
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=13,
        textColor=colors.HexColor('#8899aa'),
        spaceAfter=18,
        alignment=TA_LEFT,
        fontName='Helvetica-Oblique'
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7c8f'),
        spaceAfter=0,
        alignment=TA_LEFT,
        fontName='Helvetica',
        letterSpacing=1.5
    )
    
    coverage_style = ParagraphStyle(
        'CoverageStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#5a4a3a'),
        spaceAfter=0,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    category_label_style = ParagraphStyle(
        'CategoryLabel',
        parent=styles['Heading2'],
        fontSize=9,
        textColor=colors.HexColor('#2d6a4f'),
        spaceAfter=0,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT,
        leading=11,
        letterSpacing=2
    )
    
    source_style = ParagraphStyle(
        'SourceStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        spaceAfter=0,
        fontName='Helvetica',
        alignment=TA_RIGHT,
        leading=10
    )
    
    article_title_style = ParagraphStyle(
        'ArticleTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=10,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        leading=22,
        leftIndent=0
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading3'],
        fontSize=9,
        textColor=colors.HexColor('#2d6a4f'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        leftIndent=0,
        leading=11,
        letterSpacing=1.5
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#3a3a3a'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=15
    )
    
    italic_body_style = ParagraphStyle(
        'ItalicBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique',
        leading=15
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=4,
        leftIndent=15,
        fontName='Helvetica',
        leading=13,
        bulletIndent=5
    )
    
    cta_style = ParagraphStyle(
        'CTAStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.white,
        spaceAfter=0,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        leading=11,
        letterSpacing=1
    )
    
    # Dark header with premium newsletter design
    header_content = []
    
    # NEWSNEXUS branding with letter spacing
    branding_style = ParagraphStyle(
        'BrandingStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.white,
        spaceAfter=10,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        letterSpacing=4
    )
    
    header_content.append(Paragraph("N E W S N E X U S", branding_style))
    header_content.append(Paragraph("UPSC Daily Intelligence", title_style))
    header_content.append(Paragraph("Curated by autonomous AI agents for serious aspirants", subtitle_style))
    header_content.append(Paragraph(datetime.now().strftime("%A, %d %B %Y").upper(), date_style))
    
    # Create dark header box
    header_table_data = [[header_content[0]], [header_content[1]], [header_content[2]], [Spacer(1, 0.1*inch)], [header_content[3]]]
    header_table = Table(header_table_data, colWidths=[6.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('LEFTPADDING', (0, 0), (-1, -1), 28),
        ('RIGHTPADDING', (0, 0), (-1, -1), 28),
        ('TOPPADDING', (0, 0), (0, 0), 28),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 24),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(header_table)
    
    # Category colors - Muted, sophisticated palette
    category_colors = {
        'Polity': '#2d6a4f',
        'Economy': '#2d6a4f',
        'Environment': '#2d6a4f',
        'Science & Tech': '#6b2d8b',
        'International Relations': '#ae6100',
        'History & Culture': '#5c4033',
        'Social Issues': '#6b4226',
        'Security & Defence': '#9b2226'
    }
    
    # Count categories for coverage summary
    from collections import Counter
    category_counts = Counter(article.get('category', 'General') for article in articles)
    coverage_parts = []
    for cat, count in category_counts.most_common():
        coverage_parts.append(f"<b>{count}</b> {cat}")
    coverage_text = "Today's Coverage: " + "  |  ".join(coverage_parts)
    
    # Coverage summary box
    coverage_content = [[Paragraph(coverage_text, coverage_style)]]
    coverage_table = Table(coverage_content, colWidths=[6.5*inch])
    coverage_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f1e8')),
        ('LEFTPADDING', (0, 0), (-1, -1), 28),
        ('RIGHTPADDING', (0, 0), (-1, -1), 28),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#e0d8cc')),
    ]))
    
    story.append(coverage_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Process each article with seamless flow
    for idx, article in enumerate(articles, 1):
        category = article.get('category', 'General')
        color = colors.HexColor(category_colors.get(category, '#2d6a4f'))
        
        # Article container
        article_elements = []
        
        # Category and source header
        prelims_score = article.get('prelims_score', 'N/A')
        mains_score = article.get('mains_score', 'N/A')
        source = article.get('source', 'N/A')
        
        # Category label with source on right
        header_row_data = [[
            Paragraph(f"<b>{category.upper()}</b>", category_label_style),
            Paragraph(source, source_style)
        ]]
        header_row_table = Table(header_row_data, colWidths=[4.5*inch, 2*inch])
        header_row_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        article_elements.append(header_row_table)
        article_elements.append(Spacer(1, 0.1*inch))
        
        # Title
        title = clean_text(article.get('title', 'No Title'))
        article_elements.append(Paragraph(f"<b>{title}</b>", article_title_style))
        
        # Scores inline
        score_text = f'<font color="#999999" size=8>PRELIMS</font> <font color="#2d6a4f" size=11><b>{prelims_score}/10</b></font>     <font color="#999999" size=8>MAINS</font> <font color="#ae6100" size=11><b>{mains_score}/10</b></font>'
        score_para = Paragraph(score_text, body_style)
        article_elements.append(score_para)
        article_elements.append(Spacer(1, 0.12*inch))
        
        # Exam Angle box
        exam_angle_text = clean_text(article.get('exam_angle', 'N/A'))
        exam_angle_content = [[Paragraph(f"<b>EXAM ANGLE</b><br/><br/>{exam_angle_text}", italic_body_style)]]
        exam_angle_table = Table(exam_angle_content, colWidths=[6.5*inch])
        exam_angle_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafaf8')),
            ('LEFTPADDING', (0, 0), (-1, -1), 16),
            ('RIGHTPADDING', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LINEABOVE', (0, 0), (-1, 0), 3, color),
        ]))
        article_elements.append(exam_angle_table)
        article_elements.append(Spacer(1, 0.15*inch))
        
        # Summary
        article_elements.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", section_heading_style))
        summary_text = clean_text(article.get('summary', 'No summary available'))
        article_elements.append(Paragraph(summary_text, body_style))
        
        # Key Points
        article_elements.append(Paragraph("<b>KEY POINTS FOR REVISION</b>", section_heading_style))
        key_points = generate_key_points(article)
        for point in key_points:
            clean_point = clean_text(point)
            article_elements.append(Paragraph(f"&bull; {clean_point}", bullet_style))
        
        # Prelims Focus
        article_elements.append(Paragraph("<b>PRELIMS FOCUS</b>", section_heading_style))
        prelims_focus = clean_text(generate_prelims_focus(article))
        article_elements.append(Paragraph(prelims_focus, body_style))
        
        # Mains Dimensions
        article_elements.append(Paragraph("<b>MAINS DIMENSIONS</b>", section_heading_style))
        mains_dimensions = generate_mains_dimensions(article)
        for dimension in mains_dimensions:
            clean_dimension = clean_text(dimension)
            article_elements.append(Paragraph(f"&bull; {clean_dimension}", bullet_style))
        
        # Related Topics
        article_elements.append(Paragraph("<b>RELATED TOPICS TO REVISE</b>", section_heading_style))
        related_topics = clean_text(generate_related_topics(article))
        article_elements.append(Paragraph(related_topics, body_style))
        
        # CTA Button
        url = article.get('url', '#')
        if url != '#':
            article_elements.append(Spacer(1, 0.15*inch))
            cta_content = [[Paragraph("READ FULL ARTICLE", cta_style)]]
            cta_table = Table(cta_content, colWidths=[2*inch])
            cta_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), color),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 16),
                ('RIGHTPADDING', (0, 0), (-1, -1), 16),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            article_elements.append(cta_table)
        
        # Elegant separator (only between articles, not at end)
        if idx < len(articles):
            article_elements.append(Spacer(1, 0.3*inch))
            separator_content = [[Paragraph('<font color="#ccbbaa">◆</font>', 
                                           ParagraphStyle('SepStyle', parent=body_style, alignment=TA_CENTER, fontSize=8))]]
            separator_table = Table(separator_content, colWidths=[6.5*inch])
            separator_table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#e8e0d5')),
                ('TOPPADDING', (0, 0), (-1, -1), -6),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            article_elements.append(separator_table)
            article_elements.append(Spacer(1, 0.3*inch))
        
        # Add all article elements to story (no KeepTogether for natural flow)
        for element in article_elements:
            story.append(element)
    
    # Footer page with premium newsletter design
    story.append(PageBreak())
    story.append(Spacer(1, 2.5*inch))
    
    # Dark footer box matching header
    footer_branding_style = ParagraphStyle(
        'FooterBranding',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.white,
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        letterSpacing=4
    )
    
    footer_title_style = ParagraphStyle(
        'FooterTitle',
        parent=title_style,
        fontSize=26,
        textColor=colors.white,
        spaceAfter=8,
        alignment=TA_CENTER
    )
    
    footer_subtitle_style = ParagraphStyle(
        'FooterSubtitle',
        parent=subtitle_style,
        fontSize=11,
        textColor=colors.HexColor('#8899aa'),
        spaceAfter=14,
        alignment=TA_CENTER
    )
    
    footer_info_style = ParagraphStyle(
        'FooterInfo',
        parent=body_style,
        fontSize=9,
        textColor=colors.HexColor('#6b7c8f'),
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    footer_elements = [
        [Paragraph("N E W S N E X U S", footer_branding_style)],
        [Paragraph("Autonomous UPSC Intelligence", footer_title_style)],
        [Paragraph("Generated autonomously by the NewsNexus agentic pipeline", footer_subtitle_style)],
        [Spacer(1, 0.1*inch)],
        [Paragraph("Sources: PIB  ·  The Hindu  ·  Indian Express", footer_info_style)],
        [Paragraph(f"{len(articles)} articles analysed  ·  Top {min(len(articles), 5)} delivered", footer_info_style)]
    ]
    
    footer_table = Table(footer_elements, colWidths=[6.5*inch])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('LEFTPADDING', (0, 0), (-1, -1), 28),
        ('RIGHTPADDING', (0, 0), (-1, -1), 28),
        ('TOPPADDING', (0, 0), (0, 0), 36),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 36),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(footer_table)
    
    # Build PDF
    doc.build(story)
    logger.info(f"PDF generated: {filename}")
    
    return filename


def generate_key_points(article):
    """Generate key revision points based on article content."""
    category = article.get('category', 'General')
    
    # Generic key points based on category
    points = [
        f"Category: {category} - High relevance for UPSC syllabus",
        f"Prelims importance: {article.get('prelims_score', 0)}/10 - Focus on factual aspects",
        f"Mains importance: {article.get('mains_score', 0)}/10 - Analytical depth required"
    ]
    
    # Add source credibility
    source = article.get('source', 'Unknown')
    if source == 'PIB':
        points.append("Official government source - High credibility for factual information")
    elif source in ['The Hindu', 'Indian Express']:
        points.append(f"{source} analysis - Quality editorial perspective for mains answers")
    
    return points


def generate_prelims_focus(article):
    """Generate prelims-specific focus areas."""
    category = article.get('category', 'General')
    
    focus_map = {
        'Polity': 'Focus on constitutional provisions, amendments, judicial pronouncements, and institutional mechanisms.',
        'Economy': 'Note economic indicators, policy initiatives, budget allocations, and international economic relations.',
        'Environment': 'Remember conventions, protocols, biodiversity hotspots, and environmental legislation.',
        'Science & Tech': 'Focus on applications, government initiatives, space missions, and technological innovations.',
        'International Relations': 'Note bilateral/multilateral agreements, international organizations, and geopolitical developments.',
        'History & Culture': 'Remember historical events, cultural heritage sites, art forms, and archaeological findings.',
        'Social Issues': 'Focus on government schemes, social indicators, constitutional provisions, and welfare measures.',
        'Security & Defence': 'Note defense acquisitions, strategic partnerships, internal security challenges, and border management.'
    }
    
    return focus_map.get(category, 'Focus on factual information, dates, names, and key statistics for objective questions.')


def generate_mains_dimensions(article):
    """Generate mains answer dimensions."""
    category = article.get('category', 'General')
    
    dimensions_map = {
        'Polity': [
            'Constitutional and legal dimensions',
            'Administrative and governance aspects',
            'Judicial interpretation and precedents',
            'Federal implications and center-state relations'
        ],
        'Economy': [
            'Economic growth and development implications',
            'Fiscal and monetary policy dimensions',
            'Social equity and inclusive growth aspects',
            'International trade and competitiveness factors'
        ],
        'Environment': [
            'Environmental sustainability and conservation',
            'Climate change mitigation and adaptation',
            'Development vs. environment balance',
            'International cooperation and commitments'
        ],
        'Science & Tech': [
            'Technological innovation and applications',
            'Ethical and social implications',
            'Policy and regulatory framework',
            'India\'s position in global technology landscape'
        ],
        'International Relations': [
            'Strategic and geopolitical implications',
            'Economic and trade dimensions',
            'Regional stability and security aspects',
            'India\'s foreign policy objectives'
        ],
        'Security & Defence': [
            'National security implications',
            'Strategic autonomy and defense preparedness',
            'Internal security challenges',
            'Regional and global security architecture'
        ]
    }
    
    return dimensions_map.get(category, [
        'Policy implications and governance aspects',
        'Social and economic dimensions',
        'Challenges and way forward',
        'Best practices and recommendations'
    ])


def generate_related_topics(article):
    """Generate related topics for revision."""
    category = article.get('category', 'General')
    
    topics_map = {
        'Polity': 'Constitution (relevant parts), Landmark judgments, Parliamentary procedures, Electoral reforms',
        'Economy': 'Economic Survey, Budget provisions, RBI policies, International economic institutions',
        'Environment': 'Environmental laws, Climate agreements, Biodiversity conventions, Sustainable development',
        'Science & Tech': 'National S&T policies, Space program, Digital India, Emerging technologies',
        'International Relations': 'India\'s foreign policy, Regional organizations, Strategic partnerships, Global governance',
        'History & Culture': 'Indian heritage, Freedom movement, Art and architecture, Cultural diversity',
        'Social Issues': 'Social welfare schemes, Constitutional provisions, Social movements, Development indicators',
        'Security & Defence': 'Defense policies, Internal security acts, Border management, Strategic doctrines'
    }
    
    return topics_map.get(category, 'Review related current affairs, government reports, and syllabus topics.')


if __name__ == "__main__":
    # Test PDF generation
    test_articles = [
        {
            "title": "Supreme Court Ruling on Article 370",
            "category": "Polity",
            "prelims_score": 10,
            "mains_score": 10,
            "exam_angle": "Critical constitutional development affecting federal structure and special provisions.",
            "summary": "SC upholds abrogation of Article 370, impacting Jammu & Kashmir's special status. Landmark judgment with implications for constitutional law and center-state relations.",
            "source": "Indian Express",
            "url": "https://indianexpress.com/example",
            "published": "March 25, 2026"
        },
        {
            "title": "New Digital Public Infrastructure for Healthcare",
            "category": "Science & Tech",
            "prelims_score": 9,
            "mains_score": 8,
            "exam_angle": "Important for understanding government's digital governance initiatives.",
            "summary": "Government launches comprehensive DPI for healthcare under Ayushman Bharat Digital Mission.",
            "source": "PIB",
            "url": "https://pib.gov.in/example",
            "published": "March 26, 2026"
        }
    ]
    
    print("Generating test PDF...")
    generate_pdf_analysis(test_articles)
    print("PDF generated successfully!")
