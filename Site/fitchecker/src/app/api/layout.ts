import { NextApiRequest, NextApiResponse } from 'next';

type Measurement = {
    Gender?: string;
    Age?: number;
    HeadCircumference?: number;
    ShoulderWidth?: number;
    ChestWidth?: number;
    Belly?: number;
    Waist?: number;
    Hips?: number;
    ArmLength?: number;
    ShoulderToWaist?: number;
    WaistToKnee?: number;
    LegLength?: number;
    Weight?: number;
    Size?: string;
    Height: number;
};

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'GET') {
        const {
            Gender,
            Age,
            HeadCircumference,
            ShoulderWidth,
            ChestWidth,
            Belly,
            Waist,
            Hips,
            ArmLength,
            ShoulderToWaist,
            WaistToKnee,
            LegLength,
            Weight,
            Size,
            Height,
        } = req.query;

        if (!Height) {
            return res.status(400).json({ error: 'Height is a compulsory parameter' });
        }

        const measurement: Measurement = {
            Gender: Gender as string,
            Age: Age ? Number(Age) : undefined,
            HeadCircumference: HeadCircumference ? Number(HeadCircumference) : undefined,
            ShoulderWidth: ShoulderWidth ? Number(ShoulderWidth) : undefined,
            ChestWidth: ChestWidth ? Number(ChestWidth) : undefined,
            Belly: Belly ? Number(Belly) : undefined,
            Waist: Waist ? Number(Waist) : undefined,
            Hips: Hips ? Number(Hips) : undefined,
            ArmLength: ArmLength ? Number(ArmLength) : undefined,
            ShoulderToWaist: ShoulderToWaist ? Number(ShoulderToWaist) : undefined,
            WaistToKnee: WaistToKnee ? Number(WaistToKnee) : undefined,
            LegLength: LegLength ? Number(LegLength) : undefined,
            Weight: Weight ? Number(Weight) : undefined,
            Size: Size as string,
            Height: Number(Height),
        };

        return res.status(200).json([measurement]);
    } else {
        res.setHeader('Allow', ['GET']);
        return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}