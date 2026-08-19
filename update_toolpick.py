#!/usr/bin/env python3
"""Update ToolPick AI's standalone index.html with verified plan tiers."""

from __future__ import annotations

import json
import re
from pathlib import Path


TARGET = Path(__file__).with_name("index.html")

DATA = {
    "tools": [
        {
            "id": "chatgpt", "name": "ChatGPT", "initials": "CG", "accent": "#10a37f",
            "categories": ["AI 챗봇", "글쓰기", "리서치", "개발"], "defaultPlan": 2, "freePlan": True,
            "featuredRank": 2, "billingCurrency": "KRW",
            "score": 9.5, "bestFor": "하나로 다양한 업무를 처리하고 싶은 개인",
            "summary": "문서 작성, 데이터 분석, 이미지, 리서치와 코딩까지 폭넓은 범용 AI 도구입니다.",
            "features": ["GPT-5.6", "파일·이미지 분석", "Deep Research", "프로젝트·맞춤 GPT"],
            "caution": "한국은 KRW 결제를 지원하지만 웹·앱·계정에 따라 표시 금액이 달라질 수 있습니다.",
            "source": "https://openai.com/chatgpt/pricing/", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "텍스트 무제한* · 업로드·이미지·리서치 제한"},
                {"name": "Go", "monthly": 15000, "annualMonthly": None, "usage": "Free보다 메시지·업로드·이미지 사용량 확대"},
                {"name": "Plus", "monthly": 29000, "annualMonthly": None, "usage": "고급 추론 · 메시지·업로드·Deep Research 확대"},
                {"name": "Pro", "monthly": None, "annualMonthly": None, "usage": "Plus 대비 5× 또는 20× · 원화 결제 화면 확인"},
            ],
        },
        {
            "id": "claude", "name": "Claude", "initials": "CL", "accent": "#d97757",
            "categories": ["AI 챗봇", "글쓰기", "리서치", "개발"], "defaultPlan": 1, "freePlan": True,
            "featuredRank": 1,
            "score": 9.3, "bestFor": "긴 문서와 자연스러운 글쓰기·코딩",
            "summary": "긴 문맥 이해와 문서 작성, 코드 작업에 강하며 프로젝트와 리서치를 제공합니다.",
            "features": ["200K 컨텍스트", "Claude Code", "Research", "프로젝트·커넥터"],
            "caution": "세션·주간 한도는 대화 길이와 모델 사용량에 따라 달라집니다.",
            "source": "https://claude.com/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "기본 사용량 · 혼잡도에 따라 제한"},
                {"name": "Pro", "monthly": 20, "annualMonthly": 16.67, "usage": "표준 사용량 · 연간 $200"},
                {"name": "Max 5×", "monthly": 100, "annualMonthly": None, "usage": "Pro 대비 세션당 5× 사용량"},
                {"name": "Max 20×", "monthly": 200, "annualMonthly": None, "usage": "Pro 대비 세션당 20× 사용량"},
            ],
        },
        {
            "id": "gemini", "name": "Google Gemini", "initials": "GE", "accent": "#4285f4",
            "categories": ["AI 챗봇", "리서치", "글쓰기", "문서"], "defaultPlan": 1, "freePlan": True,
            "featuredRank": 0, "billingCurrency": "KRW",
            "score": 9.0, "bestFor": "Gmail·Docs·Drive를 많이 쓰는 사용자",
            "summary": "Google 앱 통합, 저장공간과 긴 컨텍스트를 한 구독에 묶은 AI 요금제입니다.",
            "features": ["Gemini 3.1 Pro", "Deep Research", "Google 앱 통합", "최대 1M 컨텍스트"],
            "caution": "가격과 일부 기능은 국가·언어·계정 종류에 따라 다릅니다.",
            "source": "https://one.google.com/about/google-ai-plans/", "updated": "2026-08-19",
            "plans": [
                {"name": "AI Plus", "monthly": 11000, "annualMonthly": None, "usage": "비구독자 대비 2× · 400GB"},
                {"name": "AI Pro", "monthly": 29000, "annualMonthly": None, "usage": "비구독자 대비 4× · 5TB · 1M 컨텍스트"},
                {"name": "AI Ultra 5×", "monthly": None, "annualMonthly": None, "usage": "Pro 대비 5× · 20TB · 원화 결제 화면 확인"},
                {"name": "AI Ultra 20×", "monthly": None, "annualMonthly": None, "usage": "Pro 대비 20× · 30TB · 원화 결제 화면 확인"},
            ],
        },
        {
            "id": "perplexity", "name": "Perplexity", "initials": "PX", "accent": "#20808d",
            "categories": ["리서치", "AI 챗봇"], "defaultPlan": 1, "freePlan": True,
            "score": 8.8, "bestFor": "출처를 빠르게 확인하는 웹 리서치",
            "summary": "웹 검색과 출처 제시를 중심으로 여러 고급 AI 모델을 활용하는 리서치 도구입니다.",
            "features": ["출처 기반 검색", "고급 모델 선택", "파일 분석", "Computer 크레딧"],
            "caution": "검색 결과의 원문과 인용이 실제 주장을 뒷받침하는지 확인해야 합니다.",
            "source": "https://www.perplexity.ai/help-center/en/articles/11187416-which-perplexity-subscription-plan-is-right-for-you", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "기본 검색 · 고급 검색 제한"},
                {"name": "Pro", "monthly": 20, "annualMonthly": 16.67, "usage": "고급 검색·모델 확대 · Computer 월 정액 크레딧 없음"},
                {"name": "Max", "monthly": 200, "annualMonthly": 166.67, "usage": "Model Council · Computer 10,000 크레딧/월"},
            ],
        },
        {
            "id": "kimi", "name": "Kimi K3", "initials": "K3", "accent": "#7357ff",
            "categories": ["AI 챗봇", "개발", "리서치"], "defaultPlan": 0, "freePlan": True,
            "score": 9.0, "bestFor": "긴 코드베이스·문서와 에이전트 작업",
            "summary": "네이티브 비전과 장문 처리, Kimi Code, Agent Swarm을 결합한 지식 업무·코딩형 LLM입니다.",
            "features": ["Kimi K3", "Kimi Code", "Agent Swarm", "공유 크레딧 풀"],
            "caution": "Agent 크레딧은 실제 토큰 사용량에 따라 차감됩니다.",
            "source": "https://www.kimi.com/help/membership/membership-pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Moderato", "monthly": 19, "annualMonthly": 15, "usage": "Agent 60 크레딧/월"},
                {"name": "Allegretto", "monthly": 39, "annualMonthly": 31, "usage": "Agent 150 크레딧/월"},
                {"name": "Allegro", "monthly": 99, "annualMonthly": 79, "usage": "Agent 360 크레딧/월 · K3 1M"},
                {"name": "Vivace", "monthly": 199, "annualMonthly": 159, "usage": "Agent 720 크레딧/월 · K3 1M"},
            ],
        },
        {
            "id": "grok", "name": "Grok", "initials": "GK", "accent": "#111111",
            "categories": ["AI 챗봇", "리서치", "이미지"], "defaultPlan": 1, "freePlan": True,
            "score": 8.9, "bestFor": "실시간 정보·추론과 이미지·영상 생성",
            "summary": "xAI의 최신 모델과 실시간 검색, 이미지·영상 생성, 커넥터를 묶은 범용 AI입니다.",
            "features": ["Grok 4.6", "실시간 검색", "이미지·영상 생성", "Grok Build"],
            "caution": "SuperGrok과 X Premium 계열은 기능과 결제 주체가 다릅니다.",
            "source": "https://x.ai/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "기본 사용량 · 모델·생성 한도 제한"},
                {"name": "SuperGrok", "monthly": 30, "annualMonthly": None, "usage": "상향된 Grok·이미지·영상 사용량"},
                {"name": "SuperGrok Plus", "monthly": 100, "annualMonthly": None, "usage": "대폭 상향된 사용량 · 1080p 영상 · 우선 처리"},
            ],
        },
        {
            "id": "notion", "name": "Notion", "initials": "NO", "accent": "#171717",
            "categories": ["문서", "협업", "글쓰기"], "defaultPlan": 1, "freePlan": True, "perSeat": True,
            "score": 8.7, "bestFor": "문서·프로젝트·지식을 한곳에서 관리",
            "summary": "문서와 데이터베이스, 프로젝트 관리, 에이전트를 결합한 올인원 업무 공간입니다.",
            "features": ["문서·DB", "프로젝트", "Notion Agent", "Custom Agents"],
            "caution": "Custom Agents는 기본 구독과 별도로 1,000 크레딧당 $10입니다.",
            "source": "https://www.notion.com/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "AI 제한 체험 · 파일 5MB"},
                {"name": "Plus", "monthly": 12, "annualMonthly": 10, "usage": "AI 제한 체험 · 파일 업로드 확대"},
                {"name": "Business", "monthly": 24, "annualMonthly": 20, "usage": "Notion Agent · Research · Enterprise Search"},
            ],
        },
        {
            "id": "slack", "name": "Slack", "initials": "SL", "accent": "#611f69",
            "categories": ["협업", "AI 챗봇"], "defaultPlan": 1, "freePlan": True, "perSeat": True,
            "score": 8.5, "bestFor": "대화 중심으로 일하는 팀",
            "summary": "메시지, 파일, 앱 연동과 AI 요약을 한곳에 모으는 팀 커뮤니케이션 도구입니다.",
            "features": ["메시지 검색", "앱 연동", "허들", "Slack AI"],
            "caution": "유료 플랜은 워크스페이스의 활성 사용자 수를 기준으로 청구됩니다.",
            "source": "https://slack.com/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "90일 기록 · 앱 최대 10개 · Basic AI"},
                {"name": "Pro", "monthly": 8.75, "annualMonthly": 7.25, "usage": "무제한 기록·앱 · Basic AI"},
                {"name": "Business+", "monthly": 18, "annualMonthly": 15, "usage": "Advanced AI · SSO·SCIM · 24/7 지원"},
            ],
        },
        {
            "id": "copilot", "name": "GitHub Copilot", "initials": "GH", "accent": "#6e40c9",
            "categories": ["개발", "AI 챗봇"], "defaultPlan": 1, "freePlan": True,
            "score": 9.1, "bestFor": "IDE에서 매일 코딩하는 개발자",
            "summary": "코드 완성, 에이전트, 코드 리뷰와 여러 AI 모델을 개발 환경 안에서 제공합니다.",
            "features": ["코드 완성", "코딩 에이전트", "모델 선택", "AI 크레딧"],
            "caution": "프리미엄 모델과 추가 에이전트 사용은 크레딧을 소모합니다.",
            "source": "https://github.com/features/copilot/plans", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "코드 완성 2,000회 · 채팅·Agent 50회/월"},
                {"name": "Pro", "monthly": 10, "annualMonthly": 10, "usage": "$15 월간 AI 크레딧"},
                {"name": "Pro+", "monthly": 39, "annualMonthly": None, "usage": "$70 월간 AI 크레딧 · Pro 대비 4×+"},
                {"name": "Max", "monthly": 100, "annualMonthly": None, "usage": "$200 월간 AI 크레딧 · Pro+ 대비 2.9×+"},
            ],
        },
        {
            "id": "cursor", "name": "Cursor", "initials": "CU", "accent": "#18181b",
            "categories": ["개발", "AI 챗봇"], "defaultPlan": 1, "freePlan": True,
            "score": 9.2, "bestFor": "AI 에이전트 중심으로 개발하는 사용자",
            "summary": "코드베이스를 이해하는 에이전트와 클라우드 작업, 여러 프런티어 모델을 IDE에 통합합니다.",
            "features": ["Agent", "Frontier 모델", "Cloud Agents", "MCP·Skills·Hooks"],
            "caution": "포함 사용량을 넘으면 선택적으로 온디맨드 과금이 적용될 수 있습니다.",
            "source": "https://cursor.com/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Hobby", "monthly": 0, "annualMonthly": 0, "usage": "제한된 Agent 요청"},
                {"name": "Pro", "monthly": 20, "annualMonthly": None, "usage": "Other Models $20 포함 · Agent 1×"},
                {"name": "Pro+", "monthly": 60, "annualMonthly": None, "usage": "Other Models $70 포함 · Agent 3×"},
                {"name": "Ultra", "monthly": 200, "annualMonthly": None, "usage": "Other Models $400 포함 · Agent 20×"},
            ],
        },
        {
            "id": "canva", "name": "Canva", "initials": "CA", "accent": "#7d2ae8",
            "categories": ["디자인", "이미지", "영상"], "defaultPlan": 2, "freePlan": True,
            "score": 8.9, "bestFor": "디자인·마케팅 콘텐츠를 빠르게 만드는 개인과 팀",
            "summary": "Visual Suite와 Canva AI, 브랜드 도구, 이미지·영상 제작을 한 공간에 결합합니다.",
            "features": ["Canva AI", "Visual Suite", "브랜드 도구", "이미지·영상 생성"],
            "caution": "Canva Pro는 국가별 표시 통화와 세금에 따라 가격이 달라집니다.",
            "source": "https://www.canva.com/pricing/", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "기본 AI 도구 · 사용량 제한"},
                {"name": "Pro", "monthly": None, "annualMonthly": None, "usage": "개인용 프리미엄 · 지역별 가격"},
                {"name": "Business", "monthly": 20, "annualMonthly": None, "perSeat": True, "usage": "Pro보다 높은 프리미엄 AI 한도 · 1인당"},
            ],
        },
        {
            "id": "figma", "name": "Figma AI", "initials": "FI", "accent": "#f24e1e",
            "categories": ["디자인", "개발", "이미지"], "defaultPlan": 1, "freePlan": True, "perSeat": True,
            "score": 9.0, "bestFor": "AI로 UI 디자인·프로토타입·코드 작업을 잇는 팀",
            "summary": "Figma Make, Design AI, Figma Agent와 MCP를 제품 디자인 워크플로에 결합합니다.",
            "features": ["Figma Make", "Design AI", "Figma Agent", "Figma MCP"],
            "caution": "Design AI는 유료 Full seat가 필요하며 Agent 베타는 정식 출시 후 크레딧을 소모합니다.",
            "source": "https://www.figma.com/pricing/", "updated": "2026-08-19",
            "plans": [
                {"name": "Starter", "monthly": 0, "annualMonthly": 0, "usage": "AI 150 크레딧/일 · 최대 500/월"},
                {"name": "Professional · Full", "monthly": 20, "annualMonthly": 16, "usage": "AI 3,000 크레딧/월 · 약 50~70 Make 프롬프트"},
                {"name": "Organization · Full", "monthly": 55, "annualMonthly": 55, "usage": "AI 3,500 크레딧/월 · 약 60~80 Make 프롬프트"},
                {"name": "Enterprise · Full", "monthly": 90, "annualMonthly": 90, "usage": "AI 4,250 크레딧/월 · 약 80~100 Make 프롬프트"},
            ],
        },
        {
            "id": "midjourney", "name": "Midjourney", "initials": "MJ", "accent": "#16213e",
            "categories": ["이미지", "영상"], "defaultPlan": 1, "freePlan": False,
            "score": 9.1, "bestFor": "완성도 높은 이미지와 콘셉트 비주얼 제작",
            "summary": "스타일 표현력이 강한 이미지 생성과 영상 기능을 제공하는 크리에이티브 전문 AI입니다.",
            "features": ["Fast GPU", "Relax 모드", "이미지 생성", "영상 생성"],
            "caution": "Stealth Mode와 Relax 영상 범위는 요금제별로 다릅니다.",
            "source": "https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans", "updated": "2026-08-19",
            "plans": [
                {"name": "Basic", "monthly": 10, "annualMonthly": 8, "usage": "Fast GPU 3.3시간/월"},
                {"name": "Standard", "monthly": 30, "annualMonthly": 24, "usage": "Fast GPU 15시간 · Relax 이미지 무제한"},
                {"name": "Pro", "monthly": 60, "annualMonthly": 48, "usage": "Fast GPU 30시간 · Relax 이미지·SD 영상 무제한"},
                {"name": "Mega", "monthly": 120, "annualMonthly": 96, "usage": "Fast GPU 60시간 · Relax 이미지·SD 영상 무제한"},
            ],
        },
        {
            "id": "runway", "name": "Runway", "initials": "RW", "accent": "#4f46e5",
            "categories": ["영상", "이미지", "음성"], "defaultPlan": 1, "freePlan": True,
            "score": 8.8, "bestFor": "AI 영상 제작과 이미지·오디오 편집",
            "summary": "다양한 생성 모델을 한곳에서 사용하는 영상 중심 크리에이티브 제작 플랫폼입니다.",
            "features": ["Gen-4.5", "Veo", "4K 업스케일", "영상·이미지 생성"],
            "caution": "영상 길이와 모델에 따라 크레딧 소모량이 크게 달라집니다.",
            "source": "https://runwayml.com/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "가입 시 125 크레딧 1회"},
                {"name": "Standard", "monthly": 15, "annualMonthly": 12, "usage": "625 크레딧/월"},
                {"name": "Pro", "monthly": 35, "annualMonthly": 28, "usage": "2,250 크레딧/월"},
                {"name": "Max", "monthly": 95, "annualMonthly": 76, "usage": "9,500 크레딧/월"},
            ],
        },
        {
            "id": "elevenlabs", "name": "ElevenLabs", "initials": "EL", "accent": "#1b1b1b",
            "categories": ["음성", "영상"], "defaultPlan": 2, "freePlan": True,
            "score": 8.8, "bestFor": "자연스러운 AI 음성·더빙·오디오 제작",
            "summary": "텍스트 음성 변환, 음성 복제, 더빙, 음악과 효과음을 하나의 크레딧 체계로 제공합니다.",
            "features": ["TTS", "음성 복제", "자동 더빙", "크레딧 이월"],
            "caution": "음성·음악·더빙 기능마다 크레딧 환산 방식이 다릅니다.",
            "source": "https://elevenlabs.io/pricing", "updated": "2026-08-19",
            "plans": [
                {"name": "Free", "monthly": 0, "annualMonthly": 0, "usage": "10,000 크레딧/월"},
                {"name": "Starter", "monthly": 6, "annualMonthly": 5, "usage": "30,000 크레딧/월"},
                {"name": "Creator", "monthly": 22, "annualMonthly": 18.33, "usage": "121,000 크레딧/월"},
                {"name": "Pro", "monthly": 99, "annualMonthly": 82.5, "usage": "600,000 크레딧/월"},
                {"name": "Scale", "monthly": 299, "annualMonthly": 249.17, "usage": "1.8M 크레딧/월"},
                {"name": "Business", "monthly": 990, "annualMonthly": 825, "usage": "6M 크레딧/월"},
            ],
        },
    ],
    "categories": ["전체", "AI 챗봇", "리서치", "개발", "디자인", "이미지", "영상", "음성", "글쓰기", "협업", "문서"],
}


CSS = r'''/* TOOLPICK_TIER_UPDATE_START */
.hero h1 { font-size: clamp(44px, 4.4vw, 64px); max-width: none; }
.hero h1 em { display: inline-block; white-space: nowrap; font-size: .78em; letter-spacing: -.055em; }
.plan-picker { margin: 15px 0 10px; }
.plan-picker label { display: grid; gap: 6px; color: #8d97a4; font-size: 8px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
.plan-select { width: 100%; min-height: 40px; padding: 0 34px 0 11px; border: 1px solid #dfe4eb; border-radius: 10px; outline: 0; background: #f8fafc; color: #1f2937; font-size: 11px; font-weight: 780; }
.plan-select:focus { border-color: var(--blue); box-shadow: 0 0 0 3px rgba(91, 108, 255, .09); }
.usage-note { display: flex; gap: 7px; align-items: flex-start; min-height: 36px; margin: 10px 0 13px; padding: 9px 10px; border-radius: 9px; background: #f2f5ff; color: #4d5b76; font-size: 9px; line-height: 1.55; word-break: keep-all; }
.usage-note:before { content: "사용량"; flex: 0 0 auto; color: var(--blue-dark); font-size: 8px; font-weight: 850; }
.price-prefix { color: #667085; font-size: 10px; font-weight: 750; }
.price-unavailable { font-size: 20px !important; letter-spacing: -.025em !important; }
.billing-basis { color: #9aa3af; font-size: 8px; margin-left: auto; }
.control-panel { grid-template-columns: minmax(260px, 1fr) 190px 148px; }
.auto-rate { min-height: 52px; display: grid; align-content: center; gap: 4px; border-left: 1px solid var(--line); padding: 4px 16px; }
.auto-rate span { color: #98a1ae; font-size: 8px; font-weight: 800; letter-spacing: .06em; }
.auto-rate b { color: #263449; font-size: 10px; font-variant-numeric: tabular-nums; }
@media (max-width: 720px) {
  .hero h1 { font-size: clamp(36px, 10.8vw, 45px); }
  .hero h1 em { font-size: .73em; }
  .control-panel { grid-template-columns: 1fr 1fr; }
  .search-box { grid-column: 1 / -1; }
  .auto-rate { border-top: 1px solid var(--line); border-left: 0; padding: 9px 10px 3px; }
}
/* TOOLPICK_TIER_UPDATE_END */'''


JS_TEMPLATE = r'''    "use strict";
    const DATA = __DATA__;
    const tools = DATA.tools;
    const categories = DATA.categories;
    const state = {
      query: "", category: "전체", billing: "annual", rate: 1413, rateSource: "fallback",
      sort: "score", selected: [], seats: 5,
      planIndex: Object.fromEntries(tools.map((tool) => [tool.id, tool.defaultPlan || 0]))
    };

    const $ = (selector) => document.querySelector(selector);
    const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
    const selectedPlan = (tool) => tool.plans[state.planIndex[tool.id]] || tool.plans[0];
    const monthlyPrice = (tool) => {
      const plan = selectedPlan(tool);
      if (plan.monthly === null) return null;
      return state.billing === "annual" && plan.annualMonthly !== null ? plan.annualMonthly : plan.monthly;
    };
    const isPerSeat = (tool) => selectedPlan(tool).perSeat ?? tool.perSeat ?? false;
    const billingCurrency = (tool) => tool.billingCurrency || "USD";
    const toKRW = (tool, amount) => billingCurrency(tool) === "KRW" ? amount : amount * state.rate;
    const won = (amount) => new Intl.NumberFormat("ko-KR", { maximumFractionDigits: 0 }).format(Math.round(amount / 100) * 100) + "원";
    const nativeMoney = (tool, amount) => {
      if (amount === null || !Number.isFinite(amount)) return billingCurrency(tool) === "KRW" ? "원화 가격 확인" : "가격 확인";
      return billingCurrency(tool) === "KRW"
        ? won(amount)
        : new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: amount % 1 === 0 ? 0 : 2 }).format(amount);
    };
    const money = (tool, amount) => amount === null || !Number.isFinite(amount) ? nativeMoney(tool, null) : won(toKRW(tool, amount));
    const selectedTools = () => state.selected.map((id) => tools.find((tool) => tool.id === id)).filter(Boolean);
    const totalPrice = () => selectedTools().reduce((sum, tool) => {
      const price = monthlyPrice(tool);
      return sum + (price === null ? 0 : toKRW(tool, price) * (isPerSeat(tool) ? state.seats : 1));
    }, 0);
    const hasUnknownPrice = () => selectedTools().some((tool) => monthlyPrice(tool) === null);
    const totalText = () => won(totalPrice()) + (hasUnknownPrice() ? " + 별도 확인" : "");

    function getFilteredTools() {
      const normalized = state.query.trim().toLowerCase();
      return tools.filter((tool) => state.category === "전체" || tool.categories.includes(state.category))
        .filter((tool) => {
          const planText = tool.plans.flatMap((plan) => [plan.name, plan.usage]).join(" ");
          return !normalized || [tool.name, tool.bestFor, tool.summary, planText].concat(tool.features).join(" ").toLowerCase().includes(normalized);
        })
        .sort((a, b) => {
          const featured = (a.featuredRank ?? 99) - (b.featuredRank ?? 99);
          if (featured !== 0) return featured;
          const aRaw = monthlyPrice(a);
          const bRaw = monthlyPrice(b);
          const aPrice = aRaw === null ? Number.POSITIVE_INFINITY : toKRW(a, aRaw);
          const bPrice = bRaw === null ? Number.POSITIVE_INFINITY : toKRW(b, bRaw);
          if (state.sort === "price-low") return aPrice - bPrice;
          if (state.sort === "price-high") return bPrice - aPrice;
          return b.score - a.score;
        });
    }

    function renderCategories() {
      $("#categoryRow").innerHTML = categories.map((item) =>
        '<button type="button" data-category="' + escapeHtml(item) + '" class="' + (state.category === item ? "active" : "") + '">' + escapeHtml(item) + "</button>"
      ).join("");
      $("#categoryRow").querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
        state.category = button.dataset.category;
        renderAll();
      }));
    }

    function renderTools() {
      const filtered = getFilteredTools();
      $("#resultCount").textContent = filtered.length;
      $("#emptyState").classList.toggle("hidden", filtered.length !== 0);
      $("#toolGrid").innerHTML = filtered.map((tool) => {
        const plan = selectedPlan(tool);
        const price = monthlyPrice(tool);
        const perSeat = isPerSeat(tool);
        const isSelected = state.selected.includes(tool.id);
        const disabled = !isSelected && state.selected.length >= 3;
        const saving = state.billing === "annual" && plan.monthly !== null && plan.annualMonthly !== null && plan.annualMonthly < plan.monthly
          ? '<p class="saving">연간 결제 시 월 ' + money(tool, plan.monthly - plan.annualMonthly) + " 절약</p>"
          : '<p class="saving muted">' + (state.billing === "annual" ? "연간 할인 가격 미제공" : "월간 결제 기준") + "</p>";
        const features = tool.features.map((feature) => "<li>✓ " + escapeHtml(feature) + "</li>").join("");
        const tags = tool.categories.slice(0, 3).map((item) => "<span>" + escapeHtml(item) + "</span>").join("") + (tool.freePlan ? "<span>무료 플랜</span>" : "");
        const planOptions = tool.plans.map((item, index) => '<option value="' + index + '" ' + (index === state.planIndex[tool.id] ? "selected" : "") + '>' + escapeHtml(item.name) + " · " + nativeMoney(tool, item.monthly) + "/월</option>").join("");
        const priceClass = price === null ? "price-unavailable" : "";
        const prefix = plan.pricePrefix ? '<span class="price-prefix">' + escapeHtml(plan.pricePrefix) + "</span>" : "";
        const sourcePrice = nativeMoney(tool, price);
        const basis = billingCurrency(tool) === "KRW" ? "원화 결제" : sourcePrice + " · 자동 환산";
        return '<article class="tool-card ' + (isSelected ? "selected" : "") + '">' +
          '<div class="card-top"><div class="tool-identity"><span class="tool-logo" style="background:' + tool.accent + '">' + escapeHtml(tool.initials) + '</span><div><h3>' + escapeHtml(tool.name) + '</h3><span>' + escapeHtml(plan.name) + '</span></div></div><span class="score">' + tool.score.toFixed(1) + '</span></div>' +
          '<p class="best-for">' + escapeHtml(tool.bestFor) + '</p><div class="plan-picker"><label>사용량별 요금제<select class="plan-select" data-plan-tool="' + tool.id + '">' + planOptions + '</select></label></div>' +
          '<div class="price-row">' + prefix + '<strong class="' + priceClass + '">' + money(tool, price) + '</strong><span>/ 월' + (perSeat ? " · 1인" : "") + '</span><span class="billing-basis">' + basis + "</span></div>" +
          '<p class="usage-note">' + escapeHtml(plan.usage) + '</p>' + saving + '<p class="tool-summary">' + escapeHtml(tool.summary) + '</p><ul class="feature-list">' + features + '</ul><div class="tag-row">' + tags + '</div>' +
          '<div class="card-actions"><button type="button" data-tool="' + tool.id + '" class="compare-check ' + (isSelected ? "active" : "") + '" ' + (disabled ? "disabled" : "") + '><span>' + (isSelected ? "✓" : "+") + "</span> " + (isSelected ? "비교에 담김" : disabled ? "최대 3개" : "비교에 담기") + '</button><a href="' + escapeHtml(tool.source) + '" target="_blank" rel="noopener noreferrer">공식 가격 ↗</a></div></article>';
      }).join("");
      $("#toolGrid").querySelectorAll("[data-tool]").forEach((button) => button.addEventListener("click", () => toggleSelected(button.dataset.tool)));
      $("#toolGrid").querySelectorAll("[data-plan-tool]").forEach((select) => select.addEventListener("change", () => {
        state.planIndex[select.dataset.planTool] = Number(select.value);
        renderAll();
      }));
    }

    function toggleSelected(id) {
      state.selected = state.selected.includes(id) ? state.selected.filter((item) => item !== id) : state.selected.length >= 3 ? state.selected : state.selected.concat(id);
      renderAll();
    }

    function renderTray() {
      const selected = selectedTools();
      $("#compareTray").classList.toggle("hidden", selected.length === 0);
      const selectedHtml = selected.map((tool) =>
        '<span><i style="background:' + tool.accent + '">' + escapeHtml(tool.initials) + '</i>' + escapeHtml(tool.name) + " · " + escapeHtml(selectedPlan(tool).name) + '<button type="button" data-remove="' + tool.id + '" aria-label="' + escapeHtml(tool.name) + ' 비교에서 제거">×</button></span>'
      ).join("");
      const slots = Array.from({ length: 3 - selected.length }, () => '<span class="empty-slot">도구 추가</span>').join("");
      $("#trayTools").innerHTML = selectedHtml + slots;
      $("#trayTotal").textContent = totalText() + " / 월";
      $("#openCompare").disabled = selected.length < 2;
      $("#openCompare").textContent = selected.length < 2 ? "2개 이상 선택" : "선택한 " + selected.length + "개 비교";
      $("#trayTools").querySelectorAll("[data-remove]").forEach((button) => button.addEventListener("click", () => toggleSelected(button.dataset.remove)));
    }

    function renderModal() {
      const selected = selectedTools();
      if (selected.length < 2) return;
      const cells = [];
      cells.push('<div class="table-label">도구</div>');
      selected.forEach((tool) => cells.push('<div class="table-head"><i style="background:' + tool.accent + '">' + escapeHtml(tool.initials) + '</i><b>' + escapeHtml(tool.name) + '</b><span>' + escapeHtml(selectedPlan(tool).name) + '</span></div>'));
      cells.push('<div class="table-label">월 예상 비용</div>');
      selected.forEach((tool) => {
        const price = monthlyPrice(tool);
        const total = price === null ? null : price * (isPerSeat(tool) ? state.seats : 1);
        cells.push("<div><b>" + money(tool, total) + "</b><small>" + (isPerSeat(tool) ? state.seats + "명 기준" : "개인 플랜") + "</small></div>");
      });
      cells.push('<div class="table-label">포함 사용량</div>');
      selected.forEach((tool) => cells.push("<div>" + escapeHtml(selectedPlan(tool).usage) + "</div>"));
      cells.push('<div class="table-label">추천 점수</div>');
      selected.forEach((tool) => cells.push("<div><b>" + tool.score.toFixed(1) + " / 10</b></div>"));
      cells.push('<div class="table-label">추천 대상</div>');
      selected.forEach((tool) => cells.push("<div>" + escapeHtml(tool.bestFor) + "</div>"));
      cells.push('<div class="table-label">핵심 기능</div>');
      selected.forEach((tool) => cells.push("<div><ul>" + tool.features.map((feature) => "<li>✓ " + escapeHtml(feature) + "</li>").join("") + "</ul></div>"));
      cells.push('<div class="table-label">확인할 점</div>');
      selected.forEach((tool) => cells.push("<div>" + escapeHtml(tool.caution) + "</div>"));
      $("#comparisonTable").style.setProperty("--cols", selected.length);
      $("#comparisonTable").innerHTML = cells.join("");
      $("#modalTotal").textContent = totalText();
    }

    function openModal() {
      renderModal();
      $("#modalBackdrop").classList.remove("hidden");
      document.body.classList.add("modal-open");
      $("#closeCompare").focus();
    }
    function closeModal() {
      $("#modalBackdrop").classList.add("hidden");
      document.body.classList.remove("modal-open");
    }

    function renderAll() {
      $("#monthlyBtn").classList.toggle("active", state.billing === "monthly");
      $("#annualBtn").classList.toggle("active", state.billing === "annual");
      renderCategories();
      renderTools();
      renderTray();
      if (!$("#modalBackdrop").classList.contains("hidden")) renderModal();
    }

    async function loadExchangeRate() {
      const status = $("#rateStatus");
      try {
        const response = await fetch("https://api.frankfurter.app/latest?from=USD&to=KRW", { cache: "no-store" });
        if (!response.ok) throw new Error("rate request failed");
        const data = await response.json();
        const rate = Number(data?.rates?.KRW);
        if (!Number.isFinite(rate) || rate <= 0) throw new Error("invalid rate");
        state.rate = rate;
        state.rateSource = "live";
        status.textContent = "$1 = " + new Intl.NumberFormat("ko-KR", { maximumFractionDigits: 1 }).format(rate) + "원 · 자동";
      } catch (error) {
        status.textContent = "$1 = " + new Intl.NumberFormat("ko-KR").format(state.rate) + "원 · 기준값";
      }
      renderAll();
    }

    $("#navStart").addEventListener("click", () => $("#catalog").scrollIntoView({ behavior: "smooth" }));
    $("#heroStart").addEventListener("click", () => $("#catalog").scrollIntoView({ behavior: "smooth" }));
    $("#searchInput").addEventListener("input", (event) => { state.query = event.target.value; renderTools(); });
    $("#sortSelect").addEventListener("change", (event) => { state.sort = event.target.value; renderTools(); });
    $("#monthlyBtn").addEventListener("click", () => { state.billing = "monthly"; renderAll(); });
    $("#annualBtn").addEventListener("click", () => { state.billing = "annual"; renderAll(); });
    $("#openCompare").addEventListener("click", openModal);
    $("#closeCompare").addEventListener("click", closeModal);
    $("#modalBackdrop").addEventListener("click", (event) => { if (event.target === $("#modalBackdrop")) closeModal(); });
    $("#seatInput").addEventListener("input", (event) => { state.seats = Math.max(1, Number(event.target.value) || 1); renderTray(); renderModal(); });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeModal(); });

    renderAll();
    loadExchangeRate();'''


def main() -> None:
    if not TARGET.exists():
        raise SystemExit(f"index.html을 찾을 수 없습니다: {TARGET}")

    html = TARGET.read_text(encoding="utf-8")

    marker_pattern = re.compile(
        r"\n?/\* TOOLPICK_TIER_UPDATE_START \*/.*?/\* TOOLPICK_TIER_UPDATE_END \*/\n?",
        re.DOTALL,
    )
    html = marker_pattern.sub("\n", html)
    html = html.replace("</style>", f"\n{CSS}\n  </style>", 1)

    script = JS_TEMPLATE.replace(
        "__DATA__",
        json.dumps(DATA, ensure_ascii=False, separators=(",", ":")),
    )
    script_pattern = re.compile(r"(<script>).*?(</script>)", re.DOTALL)
    if not script_pattern.search(html):
        raise SystemExit("교체할 <script> 블록을 찾지 못했습니다.")
    html = script_pattern.sub(lambda match: match.group(1) + "\n" + script + "\n  " + match.group(2), html, count=1)

    html = html.replace(
        "가격은 세금 전 공식 표시가 기준이며, 실제 한국 결제가는 다를 수 있습니다.",
        "Gemini·ChatGPT는 원화 결제가를, Claude 등 달러 결제 서비스는 자동 환산한 원화 금액을 표시합니다.",
    )
    html = html.replace("<span class=\"live-dot\">LIVE DATA</span>", "<span class=\"live-dot\">PRICE CHECK</span>")
    html = html.replace(
        '<label class="compact-control"><span>통화</span><select id="currencySelect" aria-label="통화"><option value="KRW">KRW 원화</option><option value="USD">USD 달러</option></select></label>\n'
        '        <label class="compact-control rate-control"><span>달러 환율</span><input id="rateInput" type="number" min="900" max="2500" value="1413" aria-label="달러 환율"></label>',
        '<div class="auto-rate" aria-live="polite"><span>USD → KRW 자동 환율</span><b id="rateStatus">환율 불러오는 중…</b></div>',
    )
    html = html.replace("<strong>14</strong><span>비교 도구</span>", "<strong>15</strong><span>비교 도구</span>")
    html = html.replace('id="resultCount">14</b>', 'id="resultCount">15</b>')
    TARGET.write_text(html, encoding="utf-8")
    print("완료: index.html 가격표·사용량 요금제·헤드라인 줄바꿈을 수정했습니다.")


if __name__ == "__main__":
    main()
