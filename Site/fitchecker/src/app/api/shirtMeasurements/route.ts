import { Client } from "@gradio/client";
import { NextResponse } from "next/server";

const HF_API_KEY = process.env.HF_API_KEY || "";

export async function GET(request: Request) {
	try {
		const { searchParams } = new URL(request.url);
		const height = Number(searchParams.get("height"));
		const weight = searchParams.get("weight") ? Number(searchParams.get("weight")) : null;
		const body_type = searchParams.get("body_type") || null;

		if (isNaN(height)) {
			return NextResponse.json({ error: "Height is required and must be a number" }, { status: 400 });
		}

		const client = await Client.connect("RohanVashisht/hackx", { hf_token: `hf_${HF_API_KEY}` });
		const result = await client.predict("/predict_shirt_measurements", [height, weight, body_type]);

		return NextResponse.json(result);
	} catch  {
		return NextResponse.json(
			{ error: "Failed to process request" },
			{ status: 500 }
		);
	}
}
