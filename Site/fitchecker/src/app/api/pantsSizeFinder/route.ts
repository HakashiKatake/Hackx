import { Client } from "@gradio/client";
import { NextResponse } from "next/server";

const HF_API_KEY = process.env.HF_API_KEY || "";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const waist = Number(searchParams.get("waist"));
    const leg_length = Number(searchParams.get("leg_length"));
    const hips = Number(searchParams.get("hips"));
    const timestamp = "2025-02-22 22:36:47";
    const userLogin = "RohanVashisht1234";

    // Check if all parameters are provided and valid
    if (!waist || !leg_length || !hips || isNaN(waist) || isNaN(leg_length) || isNaN(hips)) {
      return NextResponse.json(
        { error: "All parameters (waist, leg_length, hips) are required and must be valid numbers" },
        { status: 400 }
      );
    }

    const client = await Client.connect("RohanVashisht/hackx", {
      hf_token: `hf_${HF_API_KEY}`
    });

    const result = await client.predict(
      "/predict_pants_sizes",
      {
        waist,
        leg_length,
        hips
      }
    );

    return NextResponse.json({
      ...result,
      timestamp,
      userLogin
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to process request" },
      { status: 500 }
    );
  }
}