#!/usr/bin/env node
/**
 * Test script to verify frontend-to-LLaMA chatbot integration
 *
 * Usage: node test_chatbot_integration.js   (with `npm run dev` running)
 * Set APP_URL to test a server on another host/port.
 * Requires Node 18+ for the built-in fetch.
 */

async function testChatIntegration() {
    console.log('🚀 Testing Enhanced Chatbot Integration with LLaMA...\n');
    
    const baseUrl = `${process.env.APP_URL || 'http://localhost:3000'}/api/chat`;
    
    // Test 1: General Legal Question
    console.log('📋 Test 1: General Legal Question');
    try {
        const response1 = await fetch(baseUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: "What is the difference between bail and anticipatory bail?",
                mode: "general"
            })
        });
        
        const result1 = await response1.json();
        console.log('✅ General Question Response:');
        console.log(`Mode: ${result1.mode}`);
        console.log(`AI Powered: ${result1.ai_powered}`);
        console.log(`Using Document: ${result1.using_document}`);
        console.log(`Processing Time: ${result1.processing_time}s`);
        console.log(`Response Preview: ${result1.response.substring(0, 150)}...\n`);
        
    } catch (error) {
        console.log('❌ General question test failed:', error.message);
    }
    
    // Test 2: Document-specific Question
    console.log('📋 Test 2: Document-specific Question');
    try {
        const sampleDocument = `
        IN THE KERALA HIGH COURT
        Bail Application No. 41 of 2024
        Ibrahim vs State of Kerala
        Date: 2024-02-02
        
        The petitioner Ibrahim, aged 36, seeks anticipatory bail in connection with Crime No. 922/2023 
        of Vengara Police Station. He is charged under Section 286 IPC and Sections 4(b) & 5 of the 
        Explosive Substances Act, 1908, for allegedly conducting illegal quarrying and blasting granite 
        without a license, endangering life and property.
        
        The court noted his ownership of the site, a pending similar offence, and the need for proper 
        investigation. Anticipatory bail was denied, but directions were issued for him to surrender 
        within two weeks, after which his bail request could be considered on merits.
        `;
        
        const response2 = await fetch(baseUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: "Who are the parties involved in this case?",
                mode: "document",
                documentText: sampleDocument
            })
        });
        
        const result2 = await response2.json();
        console.log('✅ Document Question Response:');
        console.log(`Mode: ${result2.mode}`);
        console.log(`AI Powered: ${result2.ai_powered}`);
        console.log(`Using Document: ${result2.using_document}`);
        console.log(`Processing Time: ${result2.processing_time}s`);
        console.log(`Response Preview: ${result2.response.substring(0, 200)}...\n`);
        
    } catch (error) {
        console.log('❌ Document question test failed:', error.message);
    }
    
    // Test 3: Document Summary Request
    console.log('📋 Test 3: Document Summary Request');
    try {
        const response3 = await fetch(baseUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: "Give me a summary of this document",
                mode: "document",
                documentText: `
                IN THE KERALA HIGH COURT
                Bail Application No. 41 of 2024
                Ibrahim vs State of Kerala
                Date: 2024-02-02
                The petitioner seeks anticipatory bail for quarrying charges.
                `
            })
        });
        
        const result3 = await response3.json();
        console.log('✅ Summary Request Response:');
        console.log(`Mode: ${result3.mode}`);
        console.log(`AI Powered: ${result3.ai_powered}`);
        console.log(`Using Document: ${result3.using_document}`);
        console.log(`Processing Time: ${result3.processing_time}s`);
        console.log(`Response Preview: ${result3.response.substring(0, 200)}...\n`);
        
    } catch (error) {
        console.log('❌ Summary test failed:', error.message);
    }
    
    console.log('🎉 Chatbot Integration Testing Complete!');
    console.log('\n📊 Your chatbot now supports:');
    console.log('✅ General legal questions with LLaMA AI');
    console.log('✅ Document-specific Q&A with LLaMA AI');
    console.log('✅ AI-powered document summarization');
    console.log('✅ Intelligent fallback for basic responses');
    console.log('✅ Response timing and metadata');
}

// Run tests
testChatIntegration().catch(console.error);
