import { Client } from "@gradio/client";
import { NextResponse } from "next/server";

const HF_API_KEY = process.env.HF_API_KEY || "";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const chest = Number(searchParams.get("chest"));
    const waist = Number(searchParams.get("waist"));
    const shoulder = Number(searchParams.get("shoulder"));
    const timestamp = "2025-02-22 22:35:55";
    const userLogin = "RohanVashisht1234";

    // Check if all parameters are provided and valid
    if (!chest || !waist || !shoulder || isNaN(chest) || isNaN(waist) || isNaN(shoulder)) {
      return NextResponse.json(
        { error: "All parameters (chest, waist, shoulder) are required and must be valid numbers" },
        { status: 400 }
      );
    }

    const client = await Client.connect("RohanVashisht/hackx", {
      hf_token: `hf_${HF_API_KEY}`
    });

    const result = await client.predict(
      "/predict_brand_sizes",
      {
        chest,
        waist,
        shoulder
      }
    );

    return NextResponse.json({
      ...result,
      timestamp,
      userLogin
    });
  } catch {
    return NextResponse.json(
      { error: "Failed to process request" },
      { status: 500 }
    );
  }
}